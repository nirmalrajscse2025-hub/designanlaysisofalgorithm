comparison_count = 0
def min_max_dc(arr, low, high):
    global comparison_count
    if low == high:
        return arr[low], arr[low]
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]
    mid = (low + high) // 2
    lmin,lmax=min_max_dc(arr, low, mid)
    rmin,rmax=min_max_dc(arr, mid + 1, high)
    comparison_count+=1
    overall_min = lmin if lmin < rmin else rmin
    comparison_count+=1
    overall_max = lmax if lmax > rmax else rmax
