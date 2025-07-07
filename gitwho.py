import subprocess
from collections import defaultdict

def get_git_blame_stats():
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    files = result.stdout.strip().split('\n')

    authors = defaultdict(int)

    for file in files:
        if not file.strip():
            continue
        try:
            blame = subprocess.check_output(["git", "blame", "--line-porcelain", file])
            for line in blame.decode("utf-8").splitlines():
                if line.startswith("author "):
                    author = line[len("author "):]
                    authors[author] += 1
        except Exception:
            continue

    return sorted(authors.items(), key=lambda x: -x[1])

if __name__ == "__main__":
    print("Line-based Contributions:\n")
    for author, lines in get_git_blame_stats():
        print(f"{author}: {lines} lines")
