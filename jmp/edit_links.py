# Importing necessary modules
import sys
import os

# Checking if the script is being run from the correct directory (jmp or autoslug.github.io)
if os.path.basename(
    os.path.dirname(os.path.realpath(__file__))
) != "jmp" and "jmp" not in os.listdir("."):
    print(
        "Please run this script from the jmp directory or the autoslug.github.io repository root"
    )
    sys.exit(1)
elif "jmp" not in os.listdir("."):
    os.chdir("..")

# Checking if the user wants to add a new link
if sys.argv[1] == "add":
    # Checking if the user has provided all the required arguments
    if len(sys.argv) != 5:
        print("usage: python edit_links.py add <short> <long> <description>")
        sys.exit(1)

    # Assigning the arguments to variables
    short = sys.argv[2]
    long = sys.argv[3]
    description = sys.argv[4]

    # Generating the HTML code for the redirect
    html = '<meta http-equiv="Refresh" content="0; url=\'' + long + "'\" />"

    # Checking if the link already exists
    if short in os.listdir("."):
        print("Error: link '" + short + "' already exists")
        sys.exit(1)

    # Creating a new folder with the short name and adding an index.html file inside containing the HTML code
    os.mkdir(short)
    f = open(short + "/index.html", "w")
    f.write(html)
    f.close()

    # Adding the new link to the jmp/index.html table
    f = open("jmp/index.html", "r")
    lines = f.readlines()
    f.close()
    f = open("jmp/index.html", "w")
    for line in lines:
        # Checking if the line contains the end of the table
        if "</table>" in line:
            # Adding the new link to the table
            f.write(
                "        <tr>\n"
                + '            <th><a href="../'
                + short
                + '">'
                + short
                + "</a></th>\n"
                + "            <td>"
                + description
                + "</td>\n"
                + "        </tr>\n"
            )
        f.write(line)
    f.close()

# Checking if the user wants to delete a link
elif sys.argv[1] == "del":
    # Checking if the user has provided all the required arguments
    if len(sys.argv) != 3:
        print("usage: python edit_links.py del <short>")
        sys.exit(1)

    # Assigning the arguments to variables
    short = sys.argv[2]

    # delete folder with [short] name if it exists
    try:
        os.remove(short + "/index.html")
        os.rmdir(short)
    except FileNotFoundError:
        print("Error: link '" + short + "' does not exist")
        sys.exit(1)

    # delete link from jmp/index.html table
    f = open("jmp/index.html", "r")
    lines = f.readlines()
    f.close()
    f = open("jmp/index.html", "w")

    # parse through lines and delete the <tr> with the link
    linenum = 0
    for i, line in enumerate(lines):
        # if currently on one of the lines of the <tr> with the link, skip it
        if linenum > 0 and linenum < 4:
            linenum += 1
        # if the next line has the link, the current line is the beginning of the relevant <tr>
        elif (
            i < len(lines) - 1
            and '<th><a href="../' + short + '">' + short + "</a></th>" in lines[i + 1]
        ):
            linenum = 1
        # if the next line does not have the link or the current line is after the last line of the <tr> to be deleted, write the current line
        else:
            linenum = 0
            f.write(line)
    f.close()
