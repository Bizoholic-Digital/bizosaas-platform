vault {
  address = "http://vault:8200"
}

auto_auth {
  method "aws" {
    mount_path = "auth/aws"
    config = {
      type = "iam"
      role = "bizosaas-vault-role"
    }
  }

  sink "file" {
    config = {
      path = "/vault/agent-data/token"
    }
  }
}

cache {
  use_auto_auth_token = true
}

listener "tcp" {
  address = "127.0.0.1:8100"
  tls_disable = true
}

template {
  source      = "/vault/config/postgres.tpl"
  destination = "/vault/agent-data/postgres-config.env"
  perms       = 0644
  command     = "restart-postgres"
}

template {
  source      = "/vault/config/django.tpl"
  destination = "/vault/agent-data/django-secrets.env"
  perms       = 0644
}

template {
  source      = "/vault/config/redis.tpl"
  destination = "/vault/agent-data/redis-config.env"
  perms       = 0644
}