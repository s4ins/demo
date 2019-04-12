Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "ansible_local" do |ansible|
  ansible.inventory_path = "hosts"
  ansible.limit = 'all'
  ansible.verbose = true
  ansible.install = true
  ansible.playbook = "/vagrant/jenkins.yml"
  end 
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8202, host: 8202
  config.vm.network "forwarded_port", guest: 443, host: 443
end
