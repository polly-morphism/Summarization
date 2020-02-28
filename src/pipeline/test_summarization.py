from summarizer import Summarization
from input_reader import Namespace
import torch


text = """ WASHINGTON — In a six-page invective to House Speaker Nancy Pelosi, President Donald Trump contended he has been more wronged in the impeachment proceedings than even the 17th-century women who were hanged based on dreams, visions and confessions elicited by torture.\n

"More due process was afforded to those accused in the Salem Witch Trials," the president wrote. \n

His allies have made similar arguments, though not quite so hyperbolic. They said the president has been railroaded based on hearsay evidence. They argued he has been deprived of the right to face his accusers. They claimed the House's impeachment proceedings would not have been allowed in a court of law. \n

But legal experts say this criticism, peppered with terms borrowed from criminal proceedings, is based on a misinterpretation of what the Constitution says about impeachment and how much protection it gives the president./n

The answer: Not much.\n

Like Bill Clinton in the 1990s and Andrew Johnson more than a century earlier, Trump does not have the same constitutional protection afforded to a criminal defendant, they said. \n

"The president of the United States takes the presidency conditioned on the fact that he may be subject to impeachment," said Michael Gerhardt, a University of North Carolina law professor. "He has no entitlement to demand due process." \n
"""
arguments = Namespace(
    alpha=0.95,
    batch_size=4,
    beam_size=5,
    block_trigram=True,
    compute_rouge=False,
    documents_dir="./news_sum",
    max_length=200,
    min_length=50,
    no_cuda=False,
    summaries_output_dir="./news_sum",
)

# Select device (distibuted not available)
arguments.text = text
arguments.device = torch.device("cuda")
arguments.finalize()
summarizer = Summarization()
print(summarizer(arguments))
