from database import Banco
from interface import Interface



if __name__=="__main__":
    banco=Banco()
    interface=Interface(banco)
    interface.iniciar()
