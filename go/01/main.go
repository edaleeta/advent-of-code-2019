package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const InputFile = "input.txt"

func getFuelRequirement(mass int) int { return mass/3 - 2 }

func getFuelRequirementReal(mass int) int {
	fuel := 0
	for mass > 0 {
		mass = getFuelRequirement(mass)
		fuel += mass
	}
	return fuel
}

func calcFuelTotal(calc func(int) int) int {
	total := 0
	f, err := os.Open(InputFile)

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
		total += calc(m)
	}
	return total
}

func main() {
	fmt.Println("Part 1: ", calcFuelTotal(getFuelRequirement))
	fmt.Println("Part 2: ", calcFuelTotal(getFuelRequirementReal))

	gogi := bubu{
		name:         "Gogi",
		age:          6,
		favoriteFood: "cheese",
		sound:        screechSound,
	}

	fmt.Printf("%s\n", gogi.String())
	gogi.HaveBirthday()
}

type sound string

const (
	woofSound    sound = "woof"
	meowSound    sound = "meow"
	screechSound sound = "skreeeech"
)

type bubu struct {
	name         string
	age          int
	favoriteFood string
	sound        sound
}

func (b bubu) String() string {
	return fmt.Sprintf("%s says %s", b.name, b.sound)
}

func (b *bubu) HaveBirthday() int {
	b.age += 1
	fmt.Println(b.name, " got older!")
	fmt.Println(b.name, "is now", b.age, "!")
	return b.age
}
