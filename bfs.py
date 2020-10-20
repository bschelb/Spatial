from big_map import hc_map
import math

def bfs(start, dest, speed):
        start_pos = [start["x"], start["y"]]
        dest_pos = [dest["x"], dest["y"]]
        R = len(hc_map[0])
        C = len(hc_map)
        m = hc_map
        sr = start_pos[0]
        sc = start_pos[1]
        move_count = 0
        reached_end = False
        dr = [-1, +1, 0, 0]
        dc = [0, 0, +1, -1]
        visited = [x[:] for x in [[0] * 500] * 500]
        queue = [(sr, sc)]
        prev = [x[:] for x in [[None] * 500] * 500]
        visited[sr][sc] = 1
        while len(queue) > 0 and not reached_end:
                queue_copy = []
                while (len(queue)):
                    (r, c) = queue.pop()
                    if (r,c) == (dest_pos[0],dest_pos[1]):
                        reached_end = True
                        break
                    for i in range(4):
                        rr = r + dr[i]
                        cc = c + dc[i]
                        if rr < 0 or cc < 0:
                            continue
                        if rr >= C or cc >= R:
                            continue
                        if visited[rr][cc] == 1:
                            continue
                        square_val = m[int(rr)][int(cc)]
                        if square_val == 176:
                            continue
                        queue_copy.append([rr, cc])
                        prev[rr][cc] = [r, c]
                        visited[rr][cc] = 1
                queue = queue_copy
                if not reached_end:
                    move_count += 1
        if reached_end == True:
            return [(math.ceil(move_count / speed)), reconstructPath(start_pos, dest_pos, prev)]
        else:
            #print(start_pos)
            #print(dest_pos)
            return False

def reconstructPath(start_pos, end_pos, prev):
        path = []
        at = end_pos
        while at != None:
            path.append([at[0], at[1]])
            at = prev[at[0]][at[1]]
        path.reverse()
        if path[0] == start_pos:
            return path
        else:
            return False

# X IS ROW HEADER
# Y IS COLUMN HEADER
def getPath(start_pos, end_pos, speed):
        mosh = bfs(start_pos, end_pos, speed)
        #print(mosh)
        if type(mosh) == bool:
            return None
        else:
            long_path = [mosh[1]]
            final_path = []
            i = 0
            while i < len(long_path[0]):
                if i % speed == 0 or i == 0 or i == (len(long_path[0]) - 1):
                    final_path.append(long_path[0][i])
                i += 1
            return final_path
