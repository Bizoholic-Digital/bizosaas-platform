variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "region" {
  default = "ap-hyderabad-1"
}
variable "compartment_ocid" {}
variable "ssh_public_key_path" {}
variable "instance_shape" {
  default = "VM.Standard.A1.Flex"
}
variable "instance_count" {
  default = 2
}
variable "instance_ocpus" {
  default = 2
}
variable "instance_memory_in_gbs" {
  default = 12
}
variable "image_id" {
  default = "ocid1.image.oc1.ap-hyderabad-1.aaaaaaaacuor7yf7ipcymyg5frqekmiggmbisftjfvoisgdbofziostz2o3q" 
}
