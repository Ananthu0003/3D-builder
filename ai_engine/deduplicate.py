def deduplicate_lines(lines, tol=2):
    unique = []

    def close(a, b):
        return abs(a - b) <= tol

    for l in lines:
        x1, y1, x2, y2 = l
        found = False

        for u in unique:
            ux1, uy1, ux2, uy2 = u 
            if (
                close(x1, ux1) and close(y1, uy1) and
                close(x2, ux2) and close(y2, uy2)
            ) or (
                close(x1, ux2) and close(y1, uy2) and
                close(x2, ux1) and close(y2, uy1)
            ):
                found = True
                break

        if not found:
            unique.append(l)

    return unique
