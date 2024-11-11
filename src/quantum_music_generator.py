import logging
import os
import random

from pydub import AudioSegment
from pydub.generators import Sine
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

from src.config import note_frequencies, note_mapping

logging.basicConfig(level=logging.INFO)


class QuantumMusicGenerator:
    def __init__(
        self,
        number_of_notes: int,
        note_duration: int = 100,
        quantum_circuit: QuantumCircuit = QuantumCircuit(3, 3),
        output_path: str = "./results/quantum_generated_music.wav",
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self.number_of_notes = number_of_notes
        self.note_duration = note_duration
        self.circuit = quantum_circuit
        self.output_path = output_path
        self.logger = logger

    def synthesise(self):
        # Step 1: Apply Hadamard gates to each qubit for superposition
        self.circuit.h(0)
        self.circuit.h(1)
        self.circuit.h(2)

        # Step 2: Measure each qubit
        self.circuit.measure([0, 1, 2], [0, 1, 2])

        # Step 3: Use the Aer simulator
        simulator = Aer.get_backend("qasm_simulator")

        # Transpile the circuit for the simulator
        transpiled_circuit = transpile(self.circuit, simulator)

        # Run the circuit with self.number_of_notes shots to generate many notes
        job = simulator.run(transpiled_circuit, shots=self.number_of_notes)
        result = job.result()
        counts = result.get_counts()

        # Initialize an empty audio segment to hold the music
        audio = AudioSegment.silent(duration=0)

        # Generate and append notes to the audio segment until we reach self.number_of_notes notes
        note_count = 0
        while note_count < self.number_of_notes:
            for state, frequency in counts.items():
                if note_count >= self.number_of_notes:
                    break

                note = note_mapping[state]

                # Random chance of inserting a rest
                if random.random() < 0.2:  # 20% chance of rest
                    audio += AudioSegment.silent(duration=self.note_duration)
                else:
                    frequency = note_frequencies[note]
                    sine_wave = Sine(frequency).to_audio_segment(
                        duration=self.note_duration
                    )
                    # Apply fade in/out for smooth transitions
                    sine_wave = sine_wave.fade_in(50).fade_out(50)
                    audio += sine_wave

                note_count += 1

        # Save the generated music to a new .wav file
        output_dir = os.path.dirname(self.output_path)
        os.makedirs(output_dir, exist_ok=True)
        audio.export(self.output_path, format="wav")
        self.logger.info(f"Audio file '{self.output_path}' generated!")
