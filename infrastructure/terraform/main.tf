terraform {
  cloud {
    organization = "bizoholic-digital"
    workspaces {
      name = "bizosaas-platform-staging"
    }
  }

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.0.0"
    }
  }
}

provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# 1. VCN
resource "oci_core_vcn" "bizosaas_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "bizosaas-vcn"
  dns_label      = "bizosaas"
}

# 2. Internet Gateway
resource "oci_core_internet_gateway" "bizosaas_ig" {
  compartment_id = var.compartment_ocid
  display_name   = "bizosaas-ig"
  vcn_id         = oci_core_vcn.bizosaas_vcn.id
}

# 3. Route Table
resource "oci_core_route_table" "bizosaas_rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.bizosaas_vcn.id
  display_name   = "bizosaas-public-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.bizosaas_ig.id
  }
}

# 4. Security List
resource "oci_core_security_list" "bizosaas_sl" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.bizosaas_vcn.id
  display_name   = "bizosaas-public-sl"

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  # SSH
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  # HTTP
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 80
      max = 80
    }
  }

  # HTTPS
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 443
      max = 443
    }
  }

  # Coolify/App Ports Range
  # Allowing standard app ports and docker swarm
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 3000
      max = 9000
    }
  }
}

# 5. Subnet
resource "oci_core_subnet" "bizosaas_subnet" {
  cidr_block        = "10.0.1.0/24"
  display_name      = "bizosaas-public-subnet"
  dns_label         = "public"
  security_list_ids = [oci_core_security_list.bizosaas_sl.id]
  compartment_id    = var.compartment_ocid
  vcn_id            = oci_core_vcn.bizosaas_vcn.id
  route_table_id    = oci_core_route_table.bizosaas_rt.id
}

# 6. Availability Domain Check
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_ocid
}

# 7. Instances (Multi-Node)
resource "oci_core_instance" "bizosaas_brain" {
  count               = var.instance_count
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_ocid
  display_name        = "bizosaas-brain-${count.index + 1}"
  shape               = var.instance_shape

  shape_config {
    ocpus         = var.instance_ocpus
    memory_in_gbs = var.instance_memory_in_gbs
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.bizosaas_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = var.image_id
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)
  }
}

output "instance_public_ips" {
  value = {
    for instance in oci_core_instance.bizosaas_brain :
    instance.display_name => instance.public_ip
  }
}
