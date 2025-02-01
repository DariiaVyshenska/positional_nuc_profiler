class Read:
  def __init__(self, positions):
    self.nucleotides = {pos: None for pos in positions}
  
  def __repr__(self):
    return ''.join(nt if nt else 'N' for nt in self.nucleotides.values())

  def complete(self):
    return all(self.nucleotides.values())
  