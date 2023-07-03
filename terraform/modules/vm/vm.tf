resource "azurerm_network_interface" "finalNIC" {
  name                = "${var.application_type}-${var.resource_type}-NIC"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_address_id}"
  }
}

# we assume that this Custom Image already exists
data "azurerm_shared_image" "custom" {
  gallery_name        = "${var.custom_gallery_name}"
  name                = "${var.custom_image_name}"
  resource_group_name = "${var.custom_image_resource_group_name}"
}


resource "azurerm_linux_virtual_machine" "finalVM" {
  name                = "${var.application_type}-${var.resource_type}-VM"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group}"
  size                = "Standard_DS2_v2"
  admin_username      = "adminuser"
  network_interface_ids = [azurerm_network_interface.finalNIC.id]

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/authorized_keys/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  # source_image_reference {
  #   publisher = "Canonical"
  #   offer     = "0001-com-ubuntu-server-focal"
  #   sku       = "20_04-lts"
  #   version   = "latest"
  # }

  source_image_id = data.azurerm_shared_image.custom.id
}