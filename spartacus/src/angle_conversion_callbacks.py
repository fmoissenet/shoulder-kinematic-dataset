import biorbd
import numpy as np
from .enums import EulerSequence
from .utils import BiomechCoordinateSystem, mat_2_rotation


def get_angle_conversion_callback_from_tuple(tuple_factors: tuple[int, int, int]) -> callable:
    if not all([x in [-1, 1] for x in tuple_factors]):
        raise ValueError("tuple_factors must be a tuple of 1 and -1")

    return lambda rot1, rot2, rot3: (
        rot1 * tuple_factors[0],
        rot2 * tuple_factors[1],
        rot3 * tuple_factors[2],
    )


def convert_euler_angles(previous_sequence_str: str, new_sequence_str: str, rot1, rot2, rot3) -> np.ndarray:
    """Convert Euler angles from one sequence to another"""
    r = biorbd.Rotation.fromEulerAngles(np.array([rot1, rot2, rot3]), seq=previous_sequence_str)
    return biorbd.Rotation.toEulerAngles(r, seq=new_sequence_str).to_array()


def get_angle_conversion_callback_from_sequence(
    previous_sequence: EulerSequence, new_sequence: EulerSequence
) -> callable:
    # check if sequences are different
    if previous_sequence == new_sequence:
        raise ValueError("previous_sequence and new_sequence must be different")

    previous_sequence_str = previous_sequence.value.lower()
    new_sequence_str = new_sequence.value.lower()
    return lambda rot1, rot2, rot3: convert_euler_angles(previous_sequence_str, new_sequence_str, rot1, rot2, rot3)


def convert_euler_angles_and_frames_to_isb(
    previous_sequence_str: str,
    new_sequence_str: str,
    rot1,
    rot2,
    rot3,
    bsys_parent: BiomechCoordinateSystem,
    bsys_child: BiomechCoordinateSystem,
):
    rotation_matrix_object = biorbd.Rotation.fromEulerAngles(np.array([rot1, rot2, rot3]), seq=previous_sequence_str)
    rotation_matrix = rotation_matrix_object.to_array()

    # I'm pretty sure the rotation matrix is R_parent_child(rot1, rot2, rot3)
    converted_rotation_matrix = bsys_parent.get_rotation_matrix() @ rotation_matrix @ bsys_child.get_rotation_matrix().T

    new_rotation_matrix_object = mat_2_rotation(converted_rotation_matrix)
    return biorbd.Rotation.toEulerAngles(new_rotation_matrix_object, seq=new_sequence_str).to_array()


def get_angle_conversion_callback_to_isb_with_sequence(
    previous_sequence: EulerSequence,
    new_sequence: EulerSequence,
    bsys_parent: BiomechCoordinateSystem,
    bsys_child: BiomechCoordinateSystem,
) -> callable:
    """
    Get the callback to convert euler angles from a sequence to ISB sequence
    by recomputing the rotation matrix,
    and applying rotation matrix to turn the parent and the child into ISB coordinate system
    """
    if previous_sequence == new_sequence:
        raise ValueError("previous_sequence and new_sequence must be different")

    previous_sequence_str = previous_sequence.value.lower()
    new_sequence_str = new_sequence.value.lower()

    return lambda rot1, rot2, rot3: convert_euler_angles_and_frames_to_isb(
        previous_sequence_str,
        new_sequence_str,
        rot1,
        rot2,
        rot3,
        bsys_parent,
        bsys_child,
    )
