def add_data():
    with open("logfile.txt", "w") as fd:
        fd.write("add" + "\t" + "1" + "\t" + "How to get a good grade in 677 in 20 minutes a day." + "\t" + "distributed systems" + "\t" + "1000" + "\t" + "1" + "\n")
        fd.write("add" + "\t" + "2" + "\t" + "RPCs for Dummies." + "\t" + "distributed systems" + "\t" + "1000" + "\t" + "10" + "\n")
        fd.write("add" + "\t" + "3" + "\t" + "Xen and the Art of Surviving Graduate School." + "\t" + "graduate school" + "\t" + "1000" + "\t" + "100" + "\n")
        fd.write("add" + "\t" + "4" + "\t" + "Cooking for the Impatient Graduate Student." + "\t" + "graduate school" + "\t" + "1000" + "\t" "1000" + "\n")


if __name__ == "__main__":
    add_data()