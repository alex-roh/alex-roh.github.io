"""Mega Review 요구사항과 실패 경로를 실제로 검증한다."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

import ENAI607_Mega_Review as mega
import lab_strings as strings
import mini_drills as mini


class FileTests(unittest.TestCase):
    def load(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'readings.txt'
            path.write_text(text, encoding='utf-8')
            return mega.load_readings(path)

    def test_sample_data(self):
        data, invalid = mega.load_readings(mega.DATA_FILE)
        self.assertEqual(data, {'Ava':[10.,20.,30.,20.,40.], 'Ben':[5.,15.,25.], 'Cara':[8.,12.,16.]})
        self.assertEqual(invalid, 1)

    def test_blank_lines_do_not_count(self):
        self.assertEqual(self.load('\n  \n\t\n'), ({}, 0))

    def test_missing_fields_and_bad_numbers_are_whole_line_errors(self):
        data, count = self.load('A,1\nA,2,bad,3\n,4\nNameOnly\nA,\nA,5,6\n')
        self.assertEqual(data, {'A':[1.,5.,6.]})
        self.assertEqual(count, 4)

    def test_strip_and_extend(self):
        self.assertEqual(self.load(' A , 1 , 2 \n A, 3 \n'), ({'A':[1.,2.,3.]},0))

    def test_report_exact_text_and_thresholds(self):
        data, invalid = mega.load_readings(mega.DATA_FILE)
        expected = ("1. Ava: count = 5, average = 24.00, status = HIGH\n"
                    "2. Ben: count = 3, average = 15.00, status = LOW\n"
                    "3. Cara: count = 3, average = 12.00, status = LOW\n"
                    "Invalid lines: 1\nSensors with average >= 15.0: ['Ava', 'Ben']\n")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'summary.txt'
            means, selected, ordered = mega.make_report(data, invalid, path)
            self.assertEqual(path.read_text(encoding='utf-8'), expected)
            self.assertEqual(ordered,[('Ava',24.),('Ben',15.),('Cara',12.)])
            self.assertEqual(selected,['Ava','Ben'])
            self.assertEqual(means['Ava'],24.)
            mega.make_report({'Equal20':[20.], 'Equal15':[15.]},0,path)
            self.assertIn('average = 20.00, status = HIGH',path.read_text())

    def test_empty_average_rejected(self):
        with self.assertRaises(ValueError): mega.calculate_average([])


class StringTests(unittest.TestCase):
    def test_join_edges_and_separator(self):
        self.assertEqual(strings.str_join([]),'')
        self.assertEqual(strings.str_join(['A']),'A')
        self.assertEqual(strings.str_join(['A','','B'],'/'),'A//B')

    def test_insertion_edges_and_error_message(self):
        self.assertEqual(strings.str_insert('abc','X',0),'Xabc')
        self.assertEqual(strings.str_insert('abc','X',3),'abcX')
        self.assertEqual(strings.str_insert('abc','X',1),'aXbc')
        for pos in [-1,4]:
            out=io.StringIO()
            with contextlib.redirect_stdout(out): self.assertIsNone(strings.str_insert('abc','X',pos))
            self.assertEqual(out.getvalue(),'str_insert(): position input parameter out of range.\n')

    def test_palindrome_exact_comparison_and_type(self):
        self.assertTrue(strings.is_palindrome('level'))
        self.assertTrue(strings.is_palindrome(''))
        self.assertFalse(strings.is_palindrome('Level'))
        with contextlib.redirect_stdout(io.StringIO()): self.assertIsNone(strings.is_palindrome(123))

    def test_center_odd_even_and_too_short(self):
        self.assertEqual(strings.center_with_dots('Data',9),'..Data...')
        self.assertEqual(strings.center_with_dots('Data',8),'..Data..')
        self.assertEqual(strings.center_with_dots('Data',4),'Data')
        with self.assertRaises(ValueError): strings.center_with_dots('Data',3)


class SensorTests(unittest.TestCase):
    def setUp(self): mega.Sensor.next_id=0

    def test_shared_ids_and_count(self):
        a=mega.Sensor('A',[1.]);b=mega.CalibratedSensor('B',[1.],2.,3.)
        self.assertEqual((a.get_id(),b.get_id()),(0,1))
        self.assertEqual(mega.Sensor.get_sensor_count(),2)
        self.assertEqual(mega.CalibratedSensor.get_sensor_count(),2)

    def test_both_defensive_copies(self):
        original=[10.,20.];sensor=mega.Sensor('A',original);original[0]=999
        returned=sensor.get_values();returned.append(888)
        self.assertEqual(sensor.get_values(),[10.,20.])

    def test_invalid_values_do_not_mutate_or_consume_id(self):
        for value,exc in [('bad',TypeError),(-1,ValueError),(True,TypeError)]:
            with self.assertRaises(exc): mega.Sensor('Bad',[value])
        self.assertEqual(mega.Sensor.get_sensor_count(),0)
        sensor=mega.Sensor('A',[0.,2.])
        for value,exc in [('bad',TypeError),(-1,ValueError)]:
            with self.assertRaises(exc): sensor.add_value(value)
        self.assertEqual(sensor.get_values(),[0.,2.])
        sensor.add_value(4.)
        self.assertEqual(sensor.get_average(),2.)

    def test_calibrated_override_and_str(self):
        sensor=mega.CalibratedSensor('Ben',[5.,15.,25.],1.5,2.)
        self.assertEqual(sensor.get_average(),24.5)
        self.assertIn('avg=24.50',str(sensor))
        with self.assertRaises(ValueError): mega.CalibratedSensor('B',[1.],0.,2.)
        self.assertEqual(mega.Sensor.get_sensor_count(),1)


class RosterTests(unittest.TestCase):
    def test_sharing_replacement_and_nested_independence(self):
        with contextlib.redirect_stdout(io.StringIO()): s,b,c,a,p=mega.roster_demo()
        self.assertEqual(s[2]['name'],'Joel')
        self.assertEqual(s[1]['grades'],['B','C','B'])
        self.assertEqual(len(s[3]['grades']),6)
        self.assertIs(b[1],s[1]);self.assertIsNot(b[0],s[0])
        for x,y in zip(s,c): self.assertIsNot(x['grades'],y['grades'])
        self.assertEqual(s[0]['grades'][0],'B+')
        self.assertEqual(c[0]['grades'][0],'C')
        self.assertEqual(a[('ted',346)],576644)
        self.assertEqual(a[('sasha',988)],111111)
        self.assertNotIn(('gwen',172),a);self.assertEqual(len(a),4)
        self.assertEqual(p,[('cool stuff',6.87),('gadget',10.44),('widget',5.28),('widget',5.55)])


class ComplexTests(unittest.TestCase):
    def setUp(self): mega.conversion_count=0

    def test_quadrants_and_success_count(self):
        for z,angle in [(1+1j,np.pi/4),(-1+1j,3*np.pi/4),(-1-1j,-3*np.pi/4),(1-1j,-np.pi/4)]:
            result=mega.rec_to_pol(z);self.assertIs(type(result),tuple)
            self.assertAlmostEqual(result[0],np.sqrt(2));self.assertAlmostEqual(result[1],angle)
        self.assertEqual(mega.conversion_count,4)
        with self.assertRaises(TypeError): mega.rec_to_pol('bad')
        self.assertEqual(mega.conversion_count,4)

    def test_pair_prefix_short_inputs_and_zero(self):
        self.assertEqual(mega.create_tuple(['A','B'],[1j,2j],1),(('A',1j),))
        self.assertIsNone(mega.create_tuple(['A'],[1j,2j],2))
        self.assertIsNone(mega.create_tuple(['A','B'],[1j],2))
        self.assertEqual(mega.create_tuple([],[],0),())

    def test_function_objects_no_input_mutation_and_gain(self):
        values=[1+1j,3+4j];saved=values.copy()
        self.assertEqual(mega.apply_function(values,abs),[abs(x) for x in values])
        self.assertEqual(mega.conversion_count,0)
        result=mega.apply_function(values,mega.rec_to_pol)
        self.assertEqual(len(result),2);self.assertEqual(mega.conversion_count,2)
        self.assertEqual(values,saved)
        self.assertEqual(mega.apply_gain(3+4j),3+4j)
        self.assertEqual(mega.apply_gain(3+4j,gain=0.5),1.5+2j)


class DateTests(unittest.TestCase):
    def test_century_boundaries_and_all_month_ends(self):
        for year in [1600,2000,2024]: self.assertEqual(mega.Date(year,2,29).get_day(),29)
        for year in [1700,1900,2023]:
            with self.assertRaisesRegex(ValueError,'^Invalid date$'): mega.Date(year,2,29)
        for month,days in enumerate(mega.Date.DAYS_PER_MONTH,1):
            self.assertEqual(mega.Date(2023,month,days).get_day(),days)
            with self.assertRaises(ValueError): mega.Date(2023,month,days+1)

    def test_invalid_types_and_ranges(self):
        for args in [(0,1,1),(2024,0,1),(2024,13,1),(2024,2,0),(True,2,1),(2024,True,1),(2024,2,1.0)]:
            with self.subTest(args=args),self.assertRaises(ValueError): mega.Date(*args)

    def test_failed_update_preserves_all_fields_then_valid_update(self):
        date=mega.Date(2024,2,29)
        for args in [(2023,2,29),(2023,4,31),(2023,13,1)]:
            out=io.StringIO()
            with contextlib.redirect_stdout(out): self.assertFalse(date.set_date(*args))
            self.assertEqual(out.getvalue(),'Invalid date\n')
            self.assertEqual((date.get_year(),date.get_month(),date.get_day()),(2024,2,29))
        self.assertTrue(date.set_date(2023,3,1))
        self.assertEqual(str(date),'March 1, 2023')
        self.assertEqual(mega.Date.DAYS_PER_MONTH[1],28)


class NumericalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.path=Path(cls.temp.name)
        np.random.seed(607)
        with contextlib.redirect_stdout(io.StringIO()): cls.result=mega.numerical_demo(output_dir=cls.path)

    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def test_vectorized_functions_and_restored_view(self):
        r=self.result
        self.assertEqual(r['x'].shape,(500,));self.assertEqual(r['x'][0],0);self.assertEqual(r['x'][-1],10)
        np.testing.assert_allclose(r['f'],np.sin(3*r['x'])*np.exp(-r['x']/2))
        np.testing.assert_allclose(r['g'],np.cos(2*r['x'])*np.exp(-r['x']/2))
        self.assertTrue(np.shares_memory(r['f'],r['matrix']))
        self.assertEqual(r['matrix'].shape,(3,4));self.assertEqual(r['matrix'].T.shape,(4,3))

    def test_metadata_matrix_recovery_and_solve(self):
        r=self.result
        self.assertEqual((r['points'].ndim,r['points'].size,r['points'].shape),(2,10,(5,2)))
        self.assertTrue(np.issubdtype(r['points'].dtype,np.integer))
        self.assertTrue(np.issubdtype(r['points_float'].dtype,np.floating))
        np.testing.assert_allclose(r['transformed'],[[2,1],[1,2],[3,3],[5,4],[-1,1]])
        np.testing.assert_allclose(r['transformed']@r['inverse'],r['points_float'],atol=1e-12)
        self.assertAlmostEqual(r['determinant'],3.)
        np.testing.assert_allclose(r['solution'],[2.,3.])

    def test_complex_samples_and_histogram_counts(self):
        r=self.result
        self.assertEqual(r['z'].shape,(10000,));self.assertEqual(r['r'].shape,(10000,))
        np.testing.assert_allclose(r['r'],np.abs(r['z']))
        self.assertTrue(np.all(r['r']>=0))
        self.assertEqual(len(r['histogram_counts']),100);self.assertEqual(len(r['bin_edges']),101)
        self.assertEqual(r['histogram_counts'].sum(),10000)
        self.assertAlmostEqual(r['z'].real.std(),1/np.sqrt(2),delta=.025)
        self.assertAlmostEqual(r['z'].imag.std(),1/np.sqrt(2),delta=.025)

    def test_three_png_files_valid(self):
        for name in ['lab_simulation.png','lab_scatter.png','lab_bars.png']:
            pixels=mega.plt.imread(self.path/name)
            self.assertEqual(pixels.ndim,3);self.assertGreater(pixels.shape[1],500)

    def test_save_before_optional_show(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            def show():
                self.assertTrue(all((path/n).exists() for n in ['lab_simulation.png','lab_scatter.png','lab_bars.png']))
            with patch.object(mega.plt,'show',side_effect=show) as mocked,contextlib.redirect_stdout(io.StringIO()):
                mega.numerical_demo(show=True,output_dir=path)
            mocked.assert_called_once()


class GameTests(unittest.TestCase):
    def test_all_nine_decisions(self):
        expected=[['TIE','LOSS','WIN'],['WIN','TIE','LOSS'],['LOSS','WIN','TIE']]
        for p in range(3):
            for c in range(3): self.assertEqual(mega.judge_round(p,c),expected[p][c])

    def test_invalid_input_skips_random_and_counts(self):
        out=io.StringIO()
        with patch('builtins.input',side_effect=['bad','8','0','1','2','-1']),patch.object(mega.random,'randrange',side_effect=[2,2,2]) as rng,contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit) as exc: mega.play_training_game()
        self.assertEqual(exc.exception.code,0);self.assertEqual(rng.call_count,3)
        self.assertIn('Wins: 1, Losses: 1, Ties: 1, Total: 3',out.getvalue())

    def test_immediate_exit(self):
        out=io.StringIO()
        with patch('builtins.input',return_value='-1'),patch.object(mega.random,'randrange') as rng,contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit): mega.play_training_game()
        rng.assert_not_called();self.assertIn('Total: 0',out.getvalue())


class MiniTests(unittest.TestCase):
    def test_m1_slices_and_error_contract(self):
        self.assertEqual(mini.insert_text('ABCD','xy',2),'ABxyCD')
        self.assertEqual(mini.insert_text('ABCD','xy',0),'xyABCD')
        self.assertEqual(mini.insert_text('ABCD','xy',4),'ABCDxy')
        for pos in [-1,5]:
            with self.assertRaises(ValueError): mini.insert_text('ABCD','xy',pos)
        self.assertTrue(mini.is_palindrome('level'));self.assertFalse(mini.is_palindrome('Level'))

    def test_m2_independence_and_predicted_output(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out): roster,independent=mini.m2_demo()
        self.assertEqual(out.getvalue(),'[80, 90, 100]\nFalse True\n[80, 90]\nFalse False\n')
        self.assertIsNot(roster['Ava']['grades'],independent['Ava']['grades'])

    def test_m3_function_objects_defaults_and_keyword(self):
        values=[-2,-1,3]
        self.assertEqual(mini.apply_each(values,abs),[2,1,3])
        self.assertEqual(mini.apply_each(values,lambda x:mini.multiply(x)),[-4,-2,6])
        self.assertEqual(values,[-2,-1,3]);self.assertEqual(mini.multiply(5),10)
        self.assertEqual(mini.multiply(5,factor=3),15)

    def test_m4_global_count(self):
        mini.calls=0
        self.assertEqual(mini.counted_square(3),9);self.assertEqual(mini.counted_square(4),16)
        self.assertEqual(mini.calls,2)

    def test_m5_invalid_negative_then_zero(self):
        out=io.StringIO()
        with patch('builtins.input',side_effect=['hello','-1','0']),contextlib.redirect_stdout(out): self.assertEqual(mini.read_nonnegative_integer(),0)
        self.assertEqual(out.getvalue(),'Invalid integer\nNegative value\n')

    def test_m5_quit_and_script_exit(self):
        with patch('builtins.input',return_value='q'): self.assertIsNone(mini.read_nonnegative_integer())
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            with self.assertRaises(SystemExit) as exc: mini.exit_program()
        self.assertEqual(exc.exception.code,0);self.assertEqual(out.getvalue(),'Bye\n')

    def test_m6_keys_and_broadcast(self):
        with contextlib.redirect_stdout(io.StringIO()): records,result=mini.m6_demo()
        self.assertEqual(records,{('Ava',1):8,('Ben',2):10})
        np.testing.assert_array_equal(result,[[11,22,33],[14,25,36]])
        self.assertEqual(result.shape,(2,3))


if __name__=='__main__': unittest.main(verbosity=2)
