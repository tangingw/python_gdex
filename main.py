import sys
from gdextracking import track_package


def main():

    if len(sys.argv) >= 2:

        print(track_package(sys.argv[1]))

    else:
        
        print("python main.py <YOUR GDEX TRACKING CODE>")


if __name__ == "__main__":
    
    main()
