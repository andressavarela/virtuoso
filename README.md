# Virtuoso - Assistente Eletrônico
Virtuoso é um assistente eletrônico criado em Python e C, capaz de realizar atividades simples e responder a perguntas por meio de interações de voz. O projeto foi desenvolvido por Igor Marques de Sousa e Andressa Araújo Varela como parte do projeto para a disciplina de Microcontroladores e IoT.

### Requisitos

* Python
* Biblioteca speech_recognition
* Biblioteca wave
* Biblioteca pyaudio
* Biblioteca gtts
* Arduino (com o firmware adequado)
* Porta serial configurada corretamente no código (substitua 'COMX' pela porta serial correta)

### Como Usar

1. Clone o repositório do Virtuoso em sua máquina.
1. Certifique-se de que todos os requisitos estão instalados.
1. Conecte o Arduino ao seu computador.
1. Execute o script Python.
1. Ao executar o script, o Virtuoso estará pronto para receber comandos de voz. Ele pode ser ativado com os comandos 'ei assistente' ou 'assistente'. Após a ativação, o Virtuoso estará pronto para receber suas perguntas ou comandos.

Perguntas como "Quem é você?" ou "Quem te fez?" serão respondidas adequadamente pelo Virtuoso.
Você pode perguntar as horas, e o Virtuoso fornecerá a hora atual.
Para controlar um dispositivo conectado ao Arduino, você pode usar comandos como "Acenda a lâmpada" ou "Apague a lâmpada".
Importante: Certifique-se de configurar corretamente a porta serial para se comunicar com o Arduino no código do Virtuoso.

### Status do Projeto
Este projeto está encerrado e não está mais em desenvolvimento ativo. No entanto, você é livre para usá-lo e modificá-lo conforme suas necessidades.

