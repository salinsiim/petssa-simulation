def calculate_max_green(max_green, max_green_diff, priority, is_priority_enabled):
    return (max_green + max_green_diff if priority == 1 else max_green - max_green_diff) if is_priority_enabled else max_green
