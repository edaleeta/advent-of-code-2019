package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const InputFile = "input.txt"

type IntcodeMachine struct {
	memory []int
	ptr    int
}

func (m *IntcodeMachine) add() {
	locA := m.memory[m.ptr+1]
	locB := m.memory[m.ptr+2]
	locC := m.memory[m.ptr+3]

	overwriteVal := m.memory[locA] + m.memory[locB]
	m.memory[locC] = overwriteVal

	m.ptr += 4
}

func (m *IntcodeMachine) multiply() {
	locA := m.memory[m.ptr+1]
	locB := m.memory[m.ptr+2]
	locC := m.memory[m.ptr+3]

	overwriteVal := m.memory[locA] * m.memory[locB]
	m.memory[locC] = overwriteVal

	m.ptr += 4
}

func (m *IntcodeMachine) getOutput() int {
	return m.memory[0]
}

func (m *IntcodeMachine) run() {
	for m.ptr < len(m.memory) {
		opcode := m.memory[m.ptr]
		switch opcode {
		case 1:
			m.add()
		case 2:
			m.multiply()
		case 99:
			fallthrough
		default:
			return
		}
	}
}

func prepProgram(memory []int, noun int, verb int) []int {
	memCopy := make([]int, len(memory))
	copy(memCopy, memory)
	memCopy[1] = noun
	memCopy[2] = verb
	return memCopy
}

func createProgramInput(filename string) ([]int, error) {
	f, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}

	stringInput := strings.Split(string(f), ",")
	programInput := make([]int, len(stringInput))
	for i, x := range stringInput {
		programInput[i], err = strconv.Atoi(strings.TrimSpace(x))
		if err != nil {
			return nil, err
		}
	}

	return programInput, nil
}

func main() {

	programInput, err := createProgramInput(InputFile)
	if err != nil {
		panic(err)
	}

	fmt.Println(programInput)

	machine := IntcodeMachine{
		memory: prepProgram(programInput, 12, 2),
		ptr:    0,
	}

	machine.run()
	output := machine.getOutput()
	println(output)

}
