# Port-Scanner-Homemade-V1-
This is an experiment in my home lab so that I and other cybersecurity learners can experiment with their own homemade Nmap. You can learn about vulnerabilities; this is version 1, which already allows you to do most of the things that penetration testers and other cybersecurity professionals need. Read the Readme`s.txt for instructions .
Comandos de Ejecución
[python port_scanner.py {TARGET} --scan {fast }  --mode {  stealth }  --report {nombre}.html ]
                                        {inter}         {aggressive}
                                        {full }         {   audit  }


Modos de Scanneo -fast >>>> 1024 puertos
                 -inter >>> 5000 puertos
		 -full >>>> 65535 puertos

Modos de asignación threads -stealth >>>> 20
			    -audit >>>> 100
			    -aggressive >>> 500

--report >>> Genera archivo html con una plantilla ya ordenada para mostrar los puertos abiertos, sus posibles identificación (tiene los mas comunes asignados V2 mas expandible). Tambien cuenta con un nivel de riesgo para esos puertos identificados.



Esta es una  primera version donde se busca ver los puertos abiertos que tiene cada ip ya sea privada o publica para cualquier dispositivo conectado a nuestra red local. 
En la segunda version se trabajara con identificación de versiones de los servicios, agregamos scripts expandibles para identificar mas puertos.
Mucho mejor explicado el código y demás para su adaptación a gusto del Cliente.

Por ultimo el archivo auto-fix lo que hace es permitirnos utilizarlo tanto en windows como en Linux. En Linux debemos ejecutar ese archivo y concederles permisos para convertir archivos .py en ejecutables para Linux. En Windows tal como esta funciona.

Saludos, Espero su feedback.
