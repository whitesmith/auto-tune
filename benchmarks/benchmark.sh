if [[ $# -lt 1 ]]; then
  echo "Missing dataset argument, for example 'iris'"
  exit
fi

echo "## Grid search"
python src/benchmark.py --dataset $1 --search-method grid --search-grid-params "{\"kernel\": [\"rbf\"], \"C\": [0.01, 0.1, 0.5, 1, 5, 10, 20, 40, 80, 100], \"gamma\": [0.000001, 0.00001, 0.0001, 0.001]}"

read -p "Hit ENTER to continnue"

echo "## Auto Tune Search"
python src/benchmark.py --dataset $1 --search-auto-tune-params "[\"RealGene('C', scipy.stats.uniform(0.01, 100), minimum=0.0000001)\", \"RealGene('gamma', scipy.stats.uniform(0.0000001, 0.001), minimum=0.00000001)\"]" --search-auto-tune-pop-size 15 --search-auto-tune-num-child 5 --search-auto-tune-num-gen 5

