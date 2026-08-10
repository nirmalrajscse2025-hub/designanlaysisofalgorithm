"""
Ex. No. 9 - Efficient Bin Packing using Approximation Algorithm

CS5303 - DAA Lab
Chennai Institute of Technology | Dept. of CSE
"""

# Small tolerance to guard against binary floating-point rounding
# (e.g. 1.0 - 0.8 == 0.19999999999999996, not exactly 0.2), so an item
# that should exactly fit isn't rejected by a hair.
EPS = 1e-9


def first_fit(items, capacity=1.0):
    """Place each item into the first bin that has enough remaining space."""
    bins = []          # remaining space in each bin
    bin_contents = []  # items placed in each bin

    for item in items:
        placed = False
        for i, space in enumerate(bins):
            if space + EPS >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break
        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


def first_fit_decreasing(items, capacity=1.0):
    """First Fit, but items are sorted largest-first before placing."""
    return first_fit(sorted(items, reverse=True), capacity)


def best_fit_decreasing(items, capacity=1.0):
    """Sort items largest-first, then place each into the bin that will
    have the least remaining space after the item is added (tightest fit)."""
    sorted_items = sorted(items, reverse=True)
    bins = []
    bin_contents = []

    for item in sorted_items:
        best_idx = -1
        best_space = float('inf')

        for i, space in enumerate(bins):
            if space + EPS >= item and space - item < best_space:
                best_space = space - item
                best_idx = i

        if best_idx >= 0:
            bins[best_idx] -= item
            bin_contents[best_idx].append(item)
        else:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


def display_bins(label, bins):
    print(f'\n{label}: {len(bins)} bins')
    for i, b in enumerate(bins, 1):
        used = sum(b)
        bar = '#' * int(used * 20)
        print(f'  Bin {i}: {[round(x, 1) for x in b]} | Used: {used:.1f} '
              f'[{bar:<20}]')


def main():
    items = [0.5, 0.7, 0.3, 0.9, 0.2, 0.6, 0.8, 0.4, 0.1, 0.5]
    capacity = 1.0
    lower_bound = -(-sum(items) // capacity)  # Ceiling division

    print(f'Items: {items}')
    print(f'Capacity: {capacity}')
    print(f'Sum of items: {sum(items)}')
    print(f'Lower bound on bins: {int(lower_bound)}')

    ff_bins = first_fit(items, capacity)
    ffd_bins = first_fit_decreasing(items, capacity)
    bfd_bins = best_fit_decreasing(items, capacity)

    display_bins('First Fit (FF)', ff_bins)
    display_bins('First Fit Decreasing (FFD)', ffd_bins)
    display_bins('Best Fit Decreasing (BFD)', bfd_bins)

    print(f'\nSummary: Lower Bound={int(lower_bound)}, '
          f'FF={len(ff_bins)}, FFD={len(ffd_bins)}, BFD={len(bfd_bins)}')


if __name__ == '__main__':
    main()
