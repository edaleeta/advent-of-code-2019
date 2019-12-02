package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func getFuelRequirements(mass int) int { return mass/3 - 2 }

func main() {
	total := 0
	f, err := os.Open("input.txt")

	if err != nil {
		panic(err)
	}
	defer f.Close()

	s := bufio.NewScanner(f)
	s.Split(bufio.ScanLines)
	for s.Scan() {
		m, err := strconv.Atoi(s.Text())
		if err != nil {
			panic(err)
		}
		total += getFuelRequirements(m)
	}

	fmt.Println(total)
	
}
