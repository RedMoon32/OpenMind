**Instruction how to run WhatsApp bot**:

1)Download this project: https://github.com/danielcardeenas/whatsapp-framework , follow instructions of installing and configuring

2)Mark project as Source to our, then create new module in whatsapp_framework/modules, edit it as follows: 
```sh
from app.mac import mac, signals
from src.interface.whatsapp import *
```
3)Add to run.py method run:
```sh
def run():
    c = MacStack()
    c.start()
```
4)Done, run Main.py and enjoy life.
