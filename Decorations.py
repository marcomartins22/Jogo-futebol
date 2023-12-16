# Default      = "\033[39m"
# Black        = "\033[30m"
# Green        = "\033[32m"
# Yellow       = "\033[33m"
# Blue         = "\033[34m"
# Magenta      = "\033[35m"
# Cyan         = "\033[36m"
# LightGray    = "\033[37m"
# DarkGray     = "\033[90m"
# LightRed     = "\033[91m"
# LightGreen   = "\033[92m"
# LightYellow  = "\033[93m"
# LightBlue    = "\033[94m"
# LightMagenta = "\033[95m"
# LightCyan    = "\033[96m"

# Default      = "\033[39m"
# Black        = "\033[30m"
# Green        = "\033[32m"
# Yellow       = "\033[33m"
# Blue         = "\033[34m"
# Magenta      = "\033[35m"
# Cyan         = "\033[36m"
# LightGray    = "\033[37m"
# DarkGray     = "\033[90m"
# LightRed     = "\033[91m"
# LightGreen   = "\033[92m"
# LightYellow  = "\033[93m"
# LightBlue    = "\033[94m"
# LightMagenta = "\033[95m"
# LightCyan    = "\033[96m"

class Bcolors:
    okblue = '\033[94m'
    okgreen = '\033[92m'
    red = '\033[31m'
    endc = '\033[0m'
    header = '\033[95m'
    okcyan = '\033[96m'
    warning = '\033[93m'
    fail = '\033[91m'
    white = '\033[97m'
    darkGray = '\033[90m'
    bold = '\033[1m'
    magenta = '\033[35m'


logo = ('''
{}   _____                                                             
{}  / ____|                                                            
{} | (___   ___   ___ ___ ___ _ __                                     
{}  \___ \ / _ \ / __/ __/ _ \ '__|                                    
{}  ____) | (_) | (_| (_|  __/ |                                       
{} |_____/ \___/ \___\___\___|_|                                       
{} |_   _|   | |                                                       
{}   | |  ___| | __ _                                                  
{}   | | / __| |/ _` |                                                 
{}  _| |_\__ \ | (_| |                                                 
{} |_____|___/_|\__,_|                 _                 _     _
{}  / ____| |                         (_)               | |   (_)      
{} | |    | |__   __ _ _ __ ___  _ __  _  ___  _ __  ___| |__  _ _ __  
{} | |    | '_ \ / _` | '_ ` _ \| '_ \| |/ _ \| '_ \/ __| '_ \| | '_ \ 
{} | |____| | | | (_| | | | | | | |_) | | (_) | | | \__ \ | | | | |_) |
{}  \_____|_| |_|\__,_|_| |_| |_| .__/|_|\___/|_| |_|___/_| |_|_| .__/ 
{}                              | |                             | |    
{}                              |_|                             |_|    
'''.format(Bcolors.okgreen, Bcolors.okgreen, Bcolors.okgreen, Bcolors.okgreen, Bcolors.okgreen, Bcolors.okgreen,
           Bcolors.red, Bcolors.red, Bcolors.red, Bcolors.red,
           Bcolors.red, Bcolors.okblue, Bcolors.okblue, Bcolors.okblue, Bcolors.okblue, Bcolors.okblue,
           Bcolors.okblue, Bcolors.okblue, Bcolors.endc))

options = ('''
        {}[1] - Jogar Campeonato
        {}[2] - Tabela Classificativa
        {}[3] - Calendario de jogos
        {}[4] - Escolher equipas
        {}[5] - Restart
        {}[6] - Alterar nomes de equipas
        {}[7] - Sair\n
    {}{}Escolha uma opção: {}
    '''.format(Bcolors.okblue, Bcolors.okgreen, Bcolors.header, Bcolors.darkGray, Bcolors.okcyan, Bcolors.white,
               Bcolors.red, Bcolors.warning, Bcolors.bold, Bcolors.endc))
