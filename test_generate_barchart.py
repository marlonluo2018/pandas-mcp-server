import unittest
import os
from core.chart_generators.bar import BarChartGenerator

class TestBarChartGeneration(unittest.TestCase):
    def setUp(self):
        self.generator = BarChartGenerator()
        self.test_data = {
            "columns": [
                {
                    "name": "Job Role",
                    "type": "string",
                    "examples": [
                        "Application Developer-Cloud FullStack",
                        "Application Developer-IBM Cloud FullStack",
                        "Application Developer-Experience Front End",
                        "Application Developer-Azure Cloud FullStack",
                        "Application Developer-AWS Cloud FullStack",
                        "Application Developer-EAI",
                        "Application Developer-Open Source",
                        "Application Developer-Microsoft .NET",
                        "Application Developer-Generalist",
                        "Application Developer-Java & Web Technologies",
                        "Application Developer-Red Hat Cloud FullStack"
                    ]
                },
                {
                    "name": "Count",
                    "type": "number",
                    "examples": [29, 4, 2, 2, 2, 1, 1, 1, 1, 1, 1]
                }
            ]
        }

    def test_bar_chart_generation(self):
        """Test basic bar chart generation"""
        result = self.generator.generate(self.test_data, title="Job Role Distribution")
        
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertTrue(os.path.exists(result['html_path']))
        self.assertEqual(result['type'], 'bar')

    def test_bar_chart_options(self):
        """Test bar chart with custom options"""
        result = self.generator.generate(
            self.test_data,
            title="Job Role Distribution",
            options={'barWidth': 0.5}
        )
        
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertIn('chart_bar_', result['html_path'])

    def tearDown(self):
        # Clean up generated chart files
        if hasattr(self, 'result') and os.path.exists(self.result['html_path']):
            os.remove(self.result['html_path'])

if __name__ == '__main__':
    unittest.main()