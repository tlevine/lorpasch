from lorpasch import Lorpasch

def test_init():
    pass

class TestLorpasch:
    def setup(self):
        self.l = Lorpasch(('year', 'month'), ('rainfall',))
        self.l.insert(2015, 1, 3.3)
        self.l.insert(2015, 2, 8.3)
        self.l.insert(2015, 3,21.3)
        self.l.insert(2015, 4,29.3)
        self.l.insert(2015, 5,23.3)
        self.l.insert(2015, 6,17.3)

    def test_iter(self):
        pass

    def test_rollup(self):
        pass

    def test_insert(self):
        row = 2015, 7, 17.3
        new = self.l.insert(*row)
        assert len(new.df) == len(self.l.df) + 1
        assert list(new)[-1] == row

    def test__slice(self):
        observed = list(self.l._slice('month', 1))
        expected = [True, False, False, False, False, False]
        assert observed == expected

    def test_slice(self):
        observed = list(self.l.slice('month', 2))
        expected = [
            (8.3,)
        ]
        assert observed == expected

    def test_dice(self):
        observed = list(self.l.dice('month', 1, 5))
        expected = [
            (3.3,),
            (23.3,),
        ]
        assert observed == expected
