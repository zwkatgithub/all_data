import time
class Log:
    logFile = './log.txt'
    @staticmethod
    def log(from_, where, line=None):
        message = "Exception [{0}]. From {1} --> {2} : {3}\n".format(
            time.asctime(), from_, where, line
        )
        with open(Log.logFile, 'a') as f:
            f.write(message+'\n')
