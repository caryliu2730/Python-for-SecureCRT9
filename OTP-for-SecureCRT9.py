#$language = "Python3"
#$interface = "1.0"

import pyotp
def main():
        secret_with_params = "Your-TOTPKeys"
        secret = secret_with_params.split('&')[0]
        totp = pyotp.TOTP(secret)
        otp = totp.now()
        crt.Screen.Synchronous = True
        crt.Screen.WaitForString(":")
        crt.Screen.Send("Your-username\r")
        crt.Sleep(1);
        crt.Screen.WaitForString(":")
        crt.Screen.Send("Your-PASSWD"+otp+"\r")
        crt.Sleep(1);
        crt.Screen.Send("\r")
        crt.Screen.Synchronous = False
        # print("YOUR-username"+otp)
main()
