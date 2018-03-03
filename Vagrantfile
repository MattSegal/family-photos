# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    # Give the box 1GB memory
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end

    # Create the target VM
     config.vm.define "photos" do |photos|
        photos.vm.hostname = "photos"
        photos.vm.box = "ubuntu/xenial64"

        # Stop virtualbox from putting a stupid logfile in my project directory
        photos.vm.provider "virtualbox" do |vb|
            vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end

        # Configure networking
        photos.vm.network "private_network", ip: "192.168.2.2", :adapter => 2
        photos.vm.network "forwarded_port", guest: 80, host: 80
        photos.vm.network "forwarded_port", guest: 8080, host: 8080

        # Mount directories
        photos.vm.synced_folder "app/", "/srv/app/"

        # Add public SSH key so ansible works
        photos.vm.provision "shell" do |s|
            s.inline = "echo \"$1\" >> /root/.ssh/authorized_keys"
            s.args = ["ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEAoi/qJgRHBSc+4M9dAk5gamb23bnYKvyGqCVqbjS0y5uTteCpT97kOXPbDR+xl4/w1EtpCpxvo/zBNyqiS4aFowmJiiJvhwLS7J1zvNwsgPzNSr5L1G4tjnZGcQi0dFzRCcGw6ojl7Gz25OBgQ/58g4iGPo6bmCYOaEoxOmhwTAs= mattdsegal@gmail.com"]
        end
    end
end
