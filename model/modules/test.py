from data_loader import DataLoader

loaders = DataLoader(
    train_fn = './blog.refined.tok.shuf.train.tsv',
    batch_size=256,
    valid_ratio=.2,
    device=-1,
    max_vocab=999999,
    min_freq=5,
)

print("|train|=%d" % len(loaders.train_loader.dataset))
print("|valid|=%d" % len(loaders.valid_loader.dataset))

   
print("|vocab|=%d" % len(loaders.text.vocab))
print("|label|=%d" % len(loaders.label.vocab))

print(vars(loaders.label.vocab))
