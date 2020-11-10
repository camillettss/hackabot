import random, time
import json
random.seed(time.time())
from core.Errors import *
import base64

def GenKey():
    return

class Kernel():
    def __init__(self):
        self.islocked=True
        self.is_active=True
        self.ports={'80':1, '443':1}
        self.hashes={}
        [self.hashes.update({port:base64.b64encode(''.join([chr(random.randint(97,122)) for _ in range(5)]).encode()).decode()}) for port in self.ports.keys()]

class Robot():
    def __init__(self, cols:int, rows:int, image='R'):
        self.hp=100
        self.dict_pos={'x':random.randint(0,cols-1),'y':random.randint(0,rows-1)}
        self.pos=list(self.dict_pos.values())
        self.image=image
        self.commands=json.loads(open('core/Characters/cmds.json').read())['commands']
        # ---
        self.kernel=Kernel()
    
    def move(self, pos:dict): raise NotImplementedError

    def parser(self, cmd):
        _cmd=cmd.split()[0].lower()
        params=cmd.split()[1:]
        if '-h' in params:
            self.docs(_cmd)
            return
        #params=[arg.casefold() for arg in params]
        # se _cmd necessita di più parametri ritorna subito un errore
        if (_cmd in ['hack']) and len(params)<=0:
            print('[ERR] Some parameters are missing.'); return
        if not _cmd in self.commands:
            raise CommandError(cmd)
        else:
            if _cmd=='hack':
                #print(self.kernel.__dict__, params, sep='--')
                if self.kernel.ports[params[0]]==1:
                    raise HackError()
                else:
                    print('[..] Hacking on port:',params[0])
                    self.kernel.islocked=False
                    time.sleep(0.5)
                    print('[*] Successfully hacked.')
            elif _cmd=='help':
                print('[H] List of commands:'); [print('-',cmd) for cmd in self.commands]
                print('[H] Type "cmd -h" for info about cmd.')
            elif _cmd=='scan':
                print('scanning...')
                print('[*] Found ports:')
                for port in self.kernel.ports.keys():
                    print('-',port,' status:',self.kernel.ports[port])
            elif _cmd in ['destroy', 'shutdown']:
                if self.kernel.islocked: raise HackError()
                print('[..] Self-Destruction Enabled..')
                self.kernel.is_active=False
                time.sleep(0.6)
                print('[*] Bot killed.')
            elif _cmd=='hash':
                if params[0]=='-port':
                    # show mode, mostra la cifratura della porta
                    try:
                        print('[HASH]',params[1],self.kernel.hashes[str(params[1])])
                    except Exception:
                        [print('[HASH]',key,self.kernel.hashes[key]) for key in self.kernel.hashes.keys()]
                elif params[0]=='-res':
                    # map commands like: {param:val}
                    mappedparams={}
                    ncmd=cmd.lower().split()[1:]
                    for p in ncmd:
                        if not p.startswith('-'): continue
                        try:
                            mappedparams.update({p:ncmd[ncmd.index(p)+1]})
                        except: break
                    if mappedparams['-res']==base64.b64decode(self.kernel.hashes[mappedparams['-port']]).decode():
                        self.kernel.ports[mappedparams['-port']]=0
                        print('[*] Port {p} Successfully bypassed.'.format(p=mappedparams['-port']))
                    else:
                        print('[!!] Failed.')
                else:
                    try:
                        print('[HASH]',params[1],self.kernel.hashes[str(params[1])])
                    except Exception:
                        [print('[HASH]',key,self.kernel.hashes[key]) for key in self.kernel.hashes.keys()]
            elif _cmd in ['translater', 'encoder', 'decoder']:
                if _cmd=='encoder':
                    s=params[params.index('-text')+1]
                    print('[*] Encoded text: ', base64.b64encode(s).decode())
                elif _cmd=='decoder':
                    s=params[params.index('-text')+1]
                    print('[*] Decoded text: ', base64.b64decode(s).decode())
                elif _cmd=='translater':
                    if not '-mode' in params:
                        if 'encode' in params or 'decode' in params:
                            if 'encode' in params:
                                s=params[params.index('-text')+1]
                                print('[*] Encoded text: ', base64.b64encode(s).decode())
                            else:
                                s=params[params.index('-text')+1]
                                print('[*] Decoded text: ', base64.b64decode(s).decode())
    
    def docs(self, man):
        data=json.loads(open('core/Characters/cmds.json').read())
        for key in data['cheatsheet'][man]:
            print(key,'->',data['cheatsheet'][man][key])