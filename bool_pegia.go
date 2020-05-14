// Description:
// Game for 2 participants. Each  have a secret combination of N symbols, without repetinions
//    Each one, on her turn sends a guess, and the other side replies with X = Number of existinging symbols at the excast posistion, and Y = Number of existinging symbols NOT at the excast posistion


// Method
// One module is ceated with the secret as input, and replies with a score (X, Y) to each guess attempt.
// A second module generates Guesses, and manages a map where the key is a guess, and the vaule is the score for that guess( as recieved from the other party.
// The game ends when one party finds the secret of the of the other party. That party is declared as the winner.

// It will make sense to create and save a full array of all the valid (N Symbols without repetitions), and accessing those by index

// My Winning strategy:
// 1. Pick a first guess of the valid combinations Array.
// 2. With the given guess, send it over, and registster the score along with the guess.
// 3. If score is X = N, declare a win, and end the game.
// 4. From now on, pull the next valid guess. If it does NOT yeald the given scroe to any of your preveous attemts, repeat pulling. If found, go to step 2. Else got to steps 6
// 5. Go to step 2
// 6. No More valid guesses. Declare a Loss.


package main

import (
	"fmt"
    "strings"
    "log"
    "bytes"
    "io/ioutil"
    "bufio"
    "os"
    "path/filepath"
    "math/rand"
    "time"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}
// Symbols hold the range of allowed unique symbols used in a Guess
const Symbols = "ABCDEFGHIJKLMNOPQRTSUVWXYZ";
const num_of_symbols = len(Symbols)

// N is the Number of symbols in a guess
const N = 3; //len(Symbols);

// Guess is a valid combination of N Symbols
type Guess struct {
    g string
}

// Result is a valid combination of N Symbols
type Result struct {
    valid bool
    x, y int
}

// Player has a secret Guess, and keeps a map of own guesses to other player, whith their X,Y scores
// Player will generate valid guesses in order to crarck oppent Secret
type Player struct {
    secret Guess
    result_log map[string]Result
}
// Set sets the value of the quess object to the given value.
func (my_secret *Guess) Set(s string) {
    my_secret.g = s
}

// Init creates an map that holds the results
func (player *Player) Init (secret string) bool {
    fmt.Printf("Init of Player\n");

    if player.secret.Validate(secret, N)  {
        player.result_log = make(map[string]Result);
        fmt.Printf("Init of Player is Valid\n");
        return true
        }
    return false
}

// Rate runs a guess against a secret, counting full Matches and Parcial Matches
func (player *Player) Rate (guess string) Result {
    //my_symbols := [] byte (player.secret.g)

    var result Result;
    result.valid = false;
    result.x= -1;
    result.y= -1;

    var their_guess Guess
    if ! their_guess.Validate(guess, N){
        return result;
    }
    their_symbols := [] byte (their_guess.g)
    for pos, entry := range their_symbols {
        my_pos := 1+N;
        if -1 == pos {continue;}
        my_pos = strings.Index(player.secret.g, string(entry));
        if -1 == my_pos {continue} // symbol not in my secret
        result.valid = true;
        result.x = 0
        result.y = 0
        if (my_pos == pos) { result.x++; }
        result.y++;
    }
    player.result_log[their_guess.g]=result
    return result;
}
// Validate checks the value of the quess for size and allowed symbols.
func (my_secret *Guess) Validate(s string, size int) bool {
    // Reset
    my_secret.Set ("");
    if size != len(s) {
        fmt.Println("Rejecting: Have the wrong number of symbols in ", s);
        return false;
    }
    // Validating Unique symbols:
    symbols := [] byte (s)
    keys := make (map[byte]bool)
    for _, entry := range symbols {
        if _, value := keys[entry]; !value {
            keys[entry] = true
        }
    }
    if len(keys) < len(s) {
        fmt.Printf("Rejecting '%s'. Have duplicated symbols\n", s);
        return false;
    }
    var k int = 0;
    for k = 0; k < size && -1 != strings.Index(Symbols, string(s[k])); k++ {
    }
    if (size > k ) {
        fmt.Printf("Rejecting '%s'. Not ALL symbols are valid\n", s);
        return false;
    }
    my_secret.Set (s);
    return true;
}

func read_dat_file(path string) []byte {
    dat, err := ioutil.ReadFile(path)
    check(err);
    return dat;
}

func create_dat_file(path string) {
    f, err := os.Create(path)
    check(err)
    defer f.Close()

    w := bufio.NewWriter(f)
    const full_range int = num_of_symbols * num_of_symbols * num_of_symbols
    var guess [N]byte
    var testing_guess Guess;
    //var scrap_guess [N]byte = guess
    for sample := 0; sample < full_range ; sample++    {
        work_sample := sample
        var scrap_guess = guess
        for symbol_index := 0; symbol_index < N ; symbol_index++ {
            value := Symbols[ work_sample % num_of_symbols]
            scrap_guess[symbol_index] = value;
            work_sample = work_sample / num_of_symbols
        }
        var printable_guess string = ""
        for index := 0 ; index < len(scrap_guess)  ; index++ {
            printable_guess += string(scrap_guess[index])
        }
        if testing_guess.Validate(printable_guess, N) {
            _, err := w.WriteString(printable_guess + "\n")
            check(err)
            //fmt.Printf("wrote %d bytes\n", n4)
            fmt.Println(printable_guess)
        }
    }
    w.Flush()
}

func main() {

    var (
        buf    bytes.Buffer
        logger = log.New(&buf, "INFO: ", log.Lshortfile)

        infof = func(info string) {
            logger.Output(2, info)
        }
        program_file_name, _ = filepath.Abs(os.Args[0]);
        dat_file_name string = fmt.Sprintf("%s_N%d.dat", program_file_name,N)
        )

    // Command for Saving the valid GUESES when N = 3 into a file
    // run bool_pegia.go | grep -v Rejecting | egrep '^[A-Z]{3}$' > bool_pegia_N3.dat

    fmt.Printf("Program name is '%s', dat_file_name is '%s'\n", program_file_name, dat_file_name);
    //return;

    var dat []byte = read_dat_file(dat_file_name);
    var possible_solutions []string = strings.Split(strings.TrimSpace(string(dat)), "\n")
    fmt.Println(len(possible_solutions))



    var me Player;
    seed := rand.NewSource(time.Now().UnixNano())
    r := rand.New(seed)
    var dummy_secret = possible_solutions[r.Intn(len(possible_solutions))]
    if me.Init(dummy_secret) {
        fmt.Printf("Validated '%s'\n",dummy_secret);
        var my_rate = me.Rate("BZC")
        fmt.Println(my_rate)
        fmt.Println("The result of secret validity is ",my_rate.valid, my_rate.x, my_rate.y );
        fmt.Printf("The VALID results are: X=%d, O=%d\n",my_rate.x, my_rate.y);
        if my_rate.valid {
            fmt.Printf("The result X=%d, O=%d\n",my_rate.x, my_rate.y);
        }
    }
/*    else {
        fmt.Println("Failed to init my player");
    }
*/
    fmt.Println(me)
    testlog := fmt.Sprintf("Valid Symbols are: '%s', len = %d, valid size N = %d\n",Symbols, len(Symbols), N);
    infof(testlog);
    /* TESTING of code
    var secret Guess;
    secret.Validate("ABCDEFGHIJKLmNOPQRTSUVWXYZ", len(Symbols))
    if secret.Validate("CBC", N) { infof(fmt.Sprintf("secret = '%s', len = %d\n",secret.g, N)); }
    if secret.Validate("CBA", N) { infof(fmt.Sprintf("secret = '%s', len = %d\n",secret.g, N)); }
    if secret.Validate("ACB", N) { infof(fmt.Sprintf("secret = '%s', len = %d\n",secret.g, N)); }
    */
    fmt.Print(&buf);
}

