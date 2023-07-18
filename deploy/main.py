#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, CloudBackend, NamedCloudWorkspace, TerraformOutput,Token,TerraformVariable,Fn
from cdktf_cdktf_provider_digitalocean import provider as DgoProvider
from cdktf_cdktf_provider_digitalocean import droplet,data_digitalocean_ssh_keys
from cdktf_cdktf_provider_docker import provider as DockerProvider,container
import os

class InfraStack(TerraformStack):
    ip = None
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        CloudBackend(self,
          hostname='app.terraform.io',
          organization='clearpointexample',
          workspaces=NamedCloudWorkspace('clearpointexample')
)
        DgoProvider.DigitaloceanProvider(
            scope= self,
            id= id + "-provider",
            token= os.getenv("dgo_token",None)
          )
        
        key = data_digitalocean_ssh_keys.DataDigitaloceanSshKeys(
          self,
          id + "-keys-to-remove",
          filter= [data_digitalocean_ssh_keys.DataDigitaloceanSshKeysFilter( 
            key= "name",
            values= ["clearpoint"],
            all= True

          )]
        )
        
        d = droplet.Droplet(
          self,
          id + "-droplet",
          image= "docker-20-04",
          name= "clearpointExample",
          region= "syd1",
          size= "s-1vcpu-1gb",
          ssh_keys=[
              Fn.lookup(Fn.element(key.ssh_keys,0),"id",None)
          ]
        )

        self.ip = TerraformOutput(
          scope= self,
          id= id + "-ip",
          value= Token.as_string(d.ipv4_address)
        )

class AppStack(TerraformStack):
    def __init__(self, scope: Construct, id: str,ip : TerraformVariable):
        super().__init__(scope, id)

        CloudBackend(self,
          hostname='app.terraform.io',
          organization='clearpointexample',
          workspaces=NamedCloudWorkspace('app')
        )

        DockerProvider.DockerProvider(
            self,
            id = id + "-provider",
            host     = Fn.join("",["ssh://root@",Token.as_string(ip.value),":22"]),
            ssh_opts = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]
        )

        container.Container(
          self,
          id + "-container",
          image= "tlitovsk/clearpoint-sample:"+os.getenv("GITHUB_SHA","latest"),
          name= "clearpointExample",
          ports=[
            container.ContainerPorts(
              internal= 8080,
              external= 80
            )
          ]
        )



            


app = App()
d = InfraStack(app, "infra")
a = AppStack(app, "app",d.ip)

app.synth()
