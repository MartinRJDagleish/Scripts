use std::fs; 
use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("error: unable to read user input");
    println!("");
    println!("{} \n", input);

    // this does not work because the input is a string and not a path
    let file_contents = fs::read_to_string(input).expect("Unable to read file"); 
    
    for line in file_contents.lines() {
        println!("{}", line);
    }
}
