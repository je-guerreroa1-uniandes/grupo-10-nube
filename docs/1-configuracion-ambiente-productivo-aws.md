# Memorias de la configuración de la instancia de AWS (Primera entrega)

## 1) Usando la interfaz web se creo una instancia que corre Ubuntu 22.04 (1Gb Ram, 1vCpu)

- Ubuntu 22-04
- 1GB Ram, 1vCpu
- Sacamos una llave (llavemaquina.pem) para acceder a la máquina

![Screenshot1](./images/maquina-aws/Screenshot%20from%202023-04-16%2001-01-08.png)

## 2) Establecer las reglas del firewall y tamaño del storage

- 20 GB disco
- Reglas de firewall (Entrada: [0.0.0.0:22, 0.0.0.0:80], salida: [0.0.0.0:*])

![Screenshot2](./images/maquina-aws/Screenshot%20from%202023-04-16%2001-02-33.png)

Correción sobre el puerto 443, que no se usó

![Screenshot3](./images/maquina-aws/Screenshot%20from%202023-04-16%2001-02-56.png)

## 3) Evidencia de la creación exitosa de la instancia

![Screenshot10](./images/maquina-aws/Screenshot%20from%202023-04-16%2007-14-10.png)

## 4) Intentar desplegar los contenedores

![Screenshot4](./images/maquina-aws/Screenshot%20from%202023-04-16%2002-04-29.png)

## 5) Creación del token para poder acceder al registry privado

[Instrucciones para la creación del token](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic)

![Screenshot5](./images/maquina-aws/Screenshot%20from%202023-04-16%2002-28-38.png)
![Screenshot6](./images/maquina-aws/Screenshot%20from%202023-04-16%2002-30-47.png)

## 6) Logear el docker de la máquina ante el registry de GitHub 

![Screenshot7](./images/maquina-aws/Screenshot%20from%202023-04-16%2002-33-18.png)
![Screenshot8](./images/maquina-aws/Screenshot%20from%202023-04-16%2002-35-30.png)

## 7) Evidencia de la puesta en marcha de los componentes en el servidor de producción

**Nota: Ya se cuentas con mas componentes**

![Screenshot9](./images/maquina-aws/Screenshot%20from%202023-04-16%2002-39-24.png)
