import unittest
from unittest.mock import patch, MagicMock
import io

from main import calculate_score, is_valid_word, play_round, LETTER_VALUES, play_game


class TestWordGame(unittest.TestCase):

    def test_calculate_score(self):
        self.assertEqual(calculate_score('hello'),
                         LETTER_VALUES['H'] + LETTER_VALUES['E'] + LETTER_VALUES['L'] * 2 + LETTER_VALUES['O'])
        self.assertEqual(calculate_score('xyz'), LETTER_VALUES['X'] + LETTER_VALUES['Y'] + LETTER_VALUES['Z'])
        self.assertEqual(calculate_score('abc'), LETTER_VALUES['A'] + LETTER_VALUES['B'] + LETTER_VALUES['C'])

    @patch('requests.get')
    def test_is_valid_word_valid(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        self.assertTrue(is_valid_word('hello'))

    @patch('requests.get')
    def test_is_valid_word_invalid(self, mock_get):
        mock_get.return_value = MagicMock(status_code=404)
        self.assertFalse(is_valid_word('invalidword'))

    @patch('builtins.input', side_effect=['abc123', 'valid'])
    def test_play_round_non_alphabetic(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            play_round()
            self.assertIn("Please enter only alphabetic characters.", fake_output.getvalue())

    @patch('builtins.input', side_effect=['cabbage'])
    @patch('requests.get')
    @patch('time.time', return_value=100)
    def test_play_round_valid_word(self, mock_time, mock_requests, mock_input):
        mock_requests.return_value = MagicMock(status_code=200)
        result = play_round()
        self.assertGreater(result, 0)

    @patch('builtins.input', side_effect=['notacabbage'])
    @patch('requests.get')
    @patch('time.time', return_value=100)
    def test_play_round_invalid_length(self, mock_time, mock_requests, mock_input):
        mock_requests.return_value = MagicMock(status_code=200)
        result = play_round()
        self.assertNotEqual(result, 11)

    @patch('main.play_round', side_effect=[10, 15, 20])
    @patch('builtins.input', side_effect=['', '', 'q'])
    def test_play_game(self, mock_input, mock_play_round):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            play_game()
            self.assertIn("Game over! Your total score is: 45", fake_output.getvalue())


if __name__ == '__main__':
    unittest.main()
