"""
Module for generating mutation testing reports.
"""

from typing import Any, Dict, List, Union

from mutahunter.core.logger import logger
import json
import os

MUTAHUNTER_ASCII = r"""
.  . . . .-. .-. . . . . . . .-. .-. .-. 
|\/| | |  |  |-| |-| | | |\|  |  |-  |(  
'  ` `-'  '  ` ' ' ` `-' ' `  '  `-' ' ' 
"""


class MutantReport:
    """Class for generating mutation testing reports."""

    def __init__(self) -> None:
        pass

    def generate_report(
        self,
        total_cost: float,
        mutation_coverage: float,
        killed_mutants: int,
        survived_mutants: int,
        compile_error_mutants: int,
        timeout_mutants: int,
    ) -> None:
        """
        Generates a comprehensive mutation testing report.

        Args:
            total_cost (float): The total cost of mutation testing.
            mutation_coverage (float): The mutation coverage rate.
            killed_mutants (int): The number of killed mutants.
            survived_mutants (int): The number of survived mutants.
            compile_error_mutants (int): The number of compile error mutants.
            timeout_mutants (int): The number of timeout mutants.
        """
        print(MUTAHUNTER_ASCII)
        summary_text = self._format_summary(
            mutation_coverage,
            killed_mutants,
            survived_mutants,
            compile_error_mutants,
            timeout_mutants,
            total_cost,
        )
        print(summary_text)
  
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        parent_dir = os.path.dirname(base_dir)
        report_dir = os.path.join(parent_dir, "report")
        os.makedirs(report_dir, exist_ok=True)
        print(report_dir)

        report_path = os.path.join(report_dir, "mut_report.json")


        print("Creating File")
        with open(report_path, "w") as f:
            json.dump(summary_text, f, indent=4)
        

    def _get_source_code(self, file_name: str) -> str:
        with open(file_name, "r") as f:
            return f.read()

    def _format_summary(
        self,
        mutation_coverage: float,
        killed_mutants: int,
        survived_mutants: int,
        compile_error_mutants: int,
        timeout_mutants: int,
        total_cost: float,
    ) -> str:
        """
        Formats the summary data into a string.

        Args:
            data (Dict[str, Any]): Summary data including counts of different mutant statuses.
            total_cost (float): The total cost of mutation testing.
            line_rate (float): The line coverage rate.

        Returns:
            str: Formatted summary report.
        """
        mutation_coverage = f"{mutation_coverage*100:.2f}%"
        details = {
            
            "Mutation_Coverage": mutation_coverage,
            "Total_Mutants": survived_mutants + killed_mutants,
            "Survived_Mutants": survived_mutants,
            "Killed_Mutants": killed_mutants,
            "Timeout_Mutants":timeout_mutants,
            "Compile_Error_Mutants": compile_error_mutants,
            
            
        }

        return details
