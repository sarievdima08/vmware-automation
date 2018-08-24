variable "vc_host" { default = ""}
variable "vc_user" { default = ""}
variable "vc_pass" { default = ""}

variable "vc_dc" { default = ""}
variable "vc_cluster" { default = ""}
variable "vc_storage" { default = ""}

variable "vm_portgroup" { default = ""}
variable "vm_template" { default = ""}
variable "vm_hostname" { default = ""}
variable "vm_cpu" { default = ""}
variable "vm_ram" { default = ""}
variable "vm_disk_size" { default = ""}
variable "vm_ip" { default = ""}
variable "vm_ip_gw" { default = ""}
variable "vm_netmask" { default = ""}

provider "vsphere" {
  user           = "${var.vc_user}"
  password       = "${var.vc_pass}"
  vsphere_server = "${var.vc_host}"
  allow_unverified_ssl = true
}


data "vsphere_datacenter" "dc" {
  name = "${var.vc_dc}"
}

data "vsphere_datastore" "datastore" {
  name          = "${var.vc_storage}"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_compute_cluster" "cluster" {
  name          = "${var.vc_cluster}"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_network" "network" {
  name          = "${var.vm_portgroup}"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

data "vsphere_virtual_machine" "template" {
  #name          = "ubuntu-16.04"
  name          = "${var.vm_template}"
  datacenter_id = "${data.vsphere_datacenter.dc.id}"
}

resource "vsphere_virtual_machine" "vm" {
  name             = "${var.vm_hostname}"
  resource_pool_id = "${data.vsphere_compute_cluster.cluster.resource_pool_id}"
  datastore_id     = "${data.vsphere_datastore.datastore.id}"

  num_cpus = "${var.vm_cpu}"
  memory   = "${var.vm_ram}"
  guest_id = "${data.vsphere_virtual_machine.template.guest_id}"

  scsi_type = "${data.vsphere_virtual_machine.template.scsi_type}"

  network_interface {
    network_id   = "${data.vsphere_network.network.id}"
    adapter_type = "${data.vsphere_virtual_machine.template.network_interface_types[0]}"
  }

  disk {
    label            = "disk0"
    size             = "${var.vm_disk_size}"
# "${data.vsphere_virtual_machine.template.disks.0.size}"
    eagerly_scrub    = "${data.vsphere_virtual_machine.template.disks.0.eagerly_scrub}"
    thin_provisioned = "${data.vsphere_virtual_machine.template.disks.0.thin_provisioned}"
  }

  clone {
    template_uuid = "${data.vsphere_virtual_machine.template.id}"

    customize {
      linux_options {
        host_name = "${var.vm_hostname}"
        domain    = "srv.local"
      }

      network_interface {
        ipv4_address = "${var.vm_ip}"
        ipv4_netmask = "${var.vm_netmask}"
      }

      ipv4_gateway = "${var.vm_ip_gw}"
    }
  }

}
