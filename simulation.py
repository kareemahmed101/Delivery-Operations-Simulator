import simpy
import random
import numpy as np

class SimulationResults:
    def __init__(self):
        self.delivery_times = []
        self.wait_for_prep = []
        self.wait_for_driver = []
        self.delayed_orders = 0
        self.total_orders = 0
        self.completed_orders = 0
        self.incomplete_orders = 0
        self.order_log = []
        self.queue_log = []
        self.driver_util_log = []

def run_simulation(
    sim_time,
    num_restaurants,
    num_drivers,
    arrival_rate,
    prep_time_mean,
    prep_time_std,
    travel_time_mean,
    travel_time_std,
    delay_threshold,
    seed=42
):
    random.seed(seed)
    np.random.seed(seed)

    results = SimulationResults()
    env = simpy.Environment()

    restaurants = simpy.Resource(env, capacity=num_restaurants)
    drivers = simpy.Resource(env, capacity=num_drivers)

    active_orders = {}

    def log_queue():
        results.queue_log.append(
            (env.now, len(restaurants.queue), len(drivers.queue))
        )

    def log_driver_util():
        results.driver_util_log.append(
            (env.now, (drivers.count / num_drivers) * 100)
        )

    def order_process(order_id):
        arrival = env.now
        active_orders[order_id] = {"arrival": arrival, "stage": "waiting_prep"}
        wait_prep = 0
        prep = 0
        wait_driver = 0
        travel = 0

        with restaurants.request() as req:
            log_queue()
            yield req
            log_queue()

            active_orders[order_id]["stage"] = "preparing"
            wait_prep = env.now - arrival
            results.wait_for_prep.append(wait_prep)

            prep = max(0.5, random.gauss(prep_time_mean, prep_time_std))
            yield env.timeout(prep)

        prep_done = env.now
        active_orders[order_id]["stage"] = "waiting_driver"

        with drivers.request() as req:
            log_queue()
            log_driver_util()

            yield req

            log_driver_util()
            active_orders[order_id]["stage"] = "delivering"

            wait_driver = env.now - prep_done
            results.wait_for_driver.append(wait_driver)

            travel = max(1.0, random.gauss(travel_time_mean, travel_time_std))
            yield env.timeout(travel)

        total = env.now - arrival

        results.delivery_times.append(total)
        results.completed_orders += 1

        if total > delay_threshold:
            results.delayed_orders += 1

        results.order_log.append({
            "Order #": order_id,
            "Arrival": round(arrival, 2),
            "Prep Wait": round(wait_prep, 2),
            "Prep Time": round(prep, 2),
            "Driver Wait": round(wait_driver, 2),
            "Travel Time": round(travel, 2),
            "Total Time": round(total, 2),
            "Delayed": "Yes" if total > delay_threshold else "No",
            "Status": "Completed"
        })

        active_orders.pop(order_id, None)

    def generator():
        order_id = 1
        while True:
            inter = random.expovariate(arrival_rate)
            yield env.timeout(inter)

            results.total_orders += 1
            env.process(order_process(order_id))
            order_id += 1

    env.process(generator())
    env.run(until=sim_time)

    # Log incomplete orders still in-progress when simulation ended
    results.incomplete_orders = len(active_orders)
    for order_id, info in active_orders.items():
        results.order_log.append({
            "Order #": order_id,
            "Arrival": round(info["arrival"], 2),
            "Prep Wait": "—",
            "Prep Time": "—",
            "Driver Wait": "—",
            "Travel Time": "—",
            "Total Time": "—",
            "Delayed": "—",
            "Status": f"Incomplete ({info['stage']})"
        })

    # Sort order log by order number
    results.order_log.sort(key=lambda x: x["Order #"])

    return results
