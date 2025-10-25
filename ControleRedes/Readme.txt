BIBLIOTECAS:
pip install Flask mysql-connector-python

BANCO DE DADOS:
CREATE DATABASE IF NOT EXISTS rack_management;
USE rack_management;

CREATE TABLE IF NOT EXISTS devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    ip_address VARCHAR(15),
    vlan VARCHAR(50),
    configuration TEXT,
    notes TEXT
);

RODAR APLICAÇÃO:
python app.py




A Analogia do Prédio de Apartamentos
Imagine um prédio de apartamentos (o seu Switch físico):

Sem VLAN: Todos os moradores compartilham o mesmo espaço. Se um morador faz barulho (tráfego de rede), todos os outros escutam.

Com VLAN: O prédio é dividido em andares separados. O "andar" da Administração (VLAN 10) não vê nem escuta o tráfego do "andar" de Convidados (VLAN 30).

Como Funciona
Segmentação Lógica: Você atribui portas específicas do Switch a um número de VLAN (ex: Portas 1 a 10 são VLAN 10; Portas 11 a 20 são VLAN 20).

Isolamento de Tráfego: Uma vez que as portas estão em VLANs diferentes, o Switch impede a comunicação direta entre elas. O tráfego da VLAN 10 (Administração) não chega à VLAN 30 (Convidados).

Encaminhamento (O Papel do Firewall/Roteador): Para que duas VLANs diferentes conversem (por exemplo, se um computador da VLAN 10 precisar acessar um servidor na VLAN 20), o tráfego deve ser enviado a um dispositivo de Camada 3 (como o seu Firewall ou Roteador). O Firewall atua como um "porteiro" que controla e monitora a comunicação entre as VLANs.

Para que Servem as VLANs? (Benefícios)
As VLANs são cruciais para qualquer rede corporativa (como a sua clínica) e trazem três grandes vantagens:

1. Segurança (Mais Importante)
Isolamento de Dados: Ao separar as redes, você protege dados sensíveis. Por exemplo, se a rede Wi-Fi de Convidados (VLAN 30) for comprometida, os hackers não conseguem acessar automaticamente os computadores clínicos e servidores (VLAN 10).

Controle Centralizado: O Firewall pode aplicar regras de segurança diferentes para cada VLAN. Exemplo: "A VLAN de Convidados só pode acessar a Internet, nada mais."

2. Performance (Melhoria de Tráfego)
Redução de Domínio de Broadcast: Em redes, o broadcast é o tráfego que vai para todos os dispositivos (como um "grito" na rede). Redes grandes geram muito broadcast, o que degrada a performance. Cada VLAN cria um domínio de broadcast menor, tornando a rede mais rápida e eficiente.

3. Flexibilidade e Organização
Gerenciamento Lógico: Permite agrupar usuários e dispositivos por função, e não por localização física. No seu projeto:

VLAN 10: Tudo que é interno (Computadores, Impressoras).

VLAN 30: Tudo que é de Convidado/Wi-Fi.

Facilidade de Expansão: Se você abrir uma nova sala, basta conectar o novo ponto e configurá-lo na VLAN correta, sem precisar mudar fisicamente a topologia do cabeamento.

Resumindo para a Clínica
Na sua clínica, as VLANs garantem que:

A equipe de TI possa gerenciar o Switch e o Firewall (VLAN 99) sem interferência do tráfego diário.

Os dados dos pacientes e o sistema interno (VLAN 10) estejam isolados e protegidos da rede Wi-Fi que os convidados usam (VLAN 30).