import click

from src.quantum_music_generator import QuantumMusicGenerator


@click.group()
def cli():
    pass


@cli.command(
    help="Generates music leveraging quantum computing. The sound of quantum randomness."
)
@click.argument("number_of_notes", type=int)
@click.option(
    "--note-duration",
    type=int,
    default=100,
    help="The duration of each note in miliseconds",
)
@click.option(
    "--output-path",
    type=str,
    default="./results/quantum_generated_music.wav",
    help="Path to save the quantum generated music WAV file.",
)
def quantum_music_generator(number_of_notes: int, note_duration: int, output_path: str):
    qmg = QuantumMusicGenerator(
        number_of_notes=number_of_notes,
        note_duration=note_duration,
        output_path=output_path,
    )
    qmg.synthesise()


if __name__ == "__main__":
    cli()
