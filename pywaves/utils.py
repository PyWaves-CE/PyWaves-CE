import pywaves as pw

class Utils:
    def __init__(self, pywaves=pw):
        self.pywaves = pywaves

    def validateTx(self, tx):
        endpoint = f"/debug/validate"
        return self.pywaves.wrapper(endpoint, tx)

    def evaluateScript(self, address,script):
        endpoint = f"/utils/script/evaluate/{address}"        
        return self.pywaves.wrapper(endpoint, script)