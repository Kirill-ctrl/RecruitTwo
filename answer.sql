1.  SELECT DISTINCT name
    FROM passenger
    INNER JOIN pass_in_trip ON passenger.passenger_id = pass_in_trip.passenger_id
    WHERE passenger.passenger_id in (SELECT passenger_id
                                    FROM pass_in_trip
                                    GROUP BY passenger_id, place
                                    HAVING count(*)>1)



2.  SELECT time_out::date, COUNT(comp_id)
    FROM trip
    WHERE town_from = 'Rostov' AND ( time_out::date BETWEEN '2003-04-01' AND '2003-04-07' )
    GROUP BY time_out



3.  SELECT COUNT(DISTINCT(town_from, town_to))
    FROM trip, (
		    SELECT DISTINCT(town_from, town_to)
		    FROM trip
		    GROUP BY (town_from, town_to)
		    ORDER BY (town_from, town_to) DESC) as x



4.  SELECT name, maximum
    FROM(
        SELECT COUNT(x.company_name) as diff_company, name, maximum
        FROM(
            SELECT MAX(count_poletov) as maximum
            FROM(
                SELECT DISTINCT passenger.name, COUNT(pass_in_trip.passenger_id) as count_poletov
            FROM passenger
            INNER JOIN pass_in_trip ON pass_in_trip.passenger_id = passenger.passenger_id
            GROUP BY passenger.name) as x) as maxim,
        (
        SELECT DISTINCT passenger.name,
        company.name as company_name,
        passenger.passenger_id,
        COUNT(pass_in_trip.passenger_id) as count_poletov
        FROM company
        INNER JOIN trip ON company.company_id = trip.comp_id
        INNER JOIN pass_in_trip ON pass_in_trip.trip_number = trip.trip_number
        INNER JOIN passenger ON pass_in_trip.passenger_id = passenger.passenger_id
        GROUP BY passenger.passenger_id, company.name) as x
        WHERE count_poletov = maximum
        GROUP BY name, maximum) as pot
    WHERE diff_company = 1



5.  SELECT passenger.name, infor.sum_time
    FROM passenger, (
                    SELECT SUM(ABS(EXTRACT(EPOCH FROM time_in - time_out)*60)) as sum_time, i.passenger_id
                    FROM trip, (
                                SELECT x.passenger_id, y.trip_number
                                FROM (
                                      SELECT
                                      COUNT(DISTINCT(place)) as count_diff_place ,
                                      passenger_id,
                                      COUNT(pass_in_trip.passenger_id) as count_poletov
                                      FROM pass_in_trip
                                      GROUP BY passenger_id) as x,
                                     (
                                      SELECT trip_number, passenger_id
                                      FROM pass_in_trip
                                     ) as y
                                WHERE x.count_diff_place = x.count_poletov AND y.passenger_id = x.passenger_id
                                ORDER BY passenger_id) as i
                    WHERE trip.trip_number = i.trip_number
                    GROUP BY i.passenger_id) as infor
    WHERE passenger.passenger_id = infor.passenger_id



6.  SELECT COUNT (*), time_out as date
    FROM (
          SELECT COUNT(plane), time_out::date
          FROM trip
          WHERE town_from = 'Rostov' AND time_out::date in (
                                                            SELECT time_out::date
                                                            FROM trip
                                                            OFFSET 1)
          GROUP BY time_out) as top
    GROUP BY time_out



7.  SELECT i.name, i.sum_time
    FROM (
        SELECT MAX(pot1.sum_time) as sum_time_max, pot2.name, pot2.sum_time
        FROM (
              SELECT passenger.name, SUM(ABS(EXTRACT(EPOCH FROM time_in - time_out)*60)) as sum_time
              FROM trip
              INNER JOIN pass_in_trip ON pass_in_trip.trip_number = trip.trip_number
              INNER JOIN passenger ON pass_in_trip.passenger_id = passenger.passenger_id
              GROUP BY passenger.name) as pot1,
            (
              SELECT passenger.name, SUM(ABS(EXTRACT(EPOCH FROM time_in - time_out)*60)) as sum_time
              FROM trip
              INNER JOIN pass_in_trip ON pass_in_trip.trip_number = trip.trip_number
              INNER JOIN passenger ON pass_in_trip.passenger_id = passenger.passenger_id
              GROUP BY passenger.name) as pot2
              GROUP BY pot2.name, pot2.sum_time) as i
    WHERE sum_time_max = sum_time



8.  SELECT name, count
    FROM (
        SELECT name,
        COUNT(trip_number)
        FROM (
            SELECT name, trip.trip_number
            FROM trip
            INNER JOIN pass_in_trip ON pass_in_trip.trip_number = trip.trip_number
            INNER JOIN passenger ON passenger.passenger_id = pass_in_trip.passenger_id
            WHERE town_from <> 'Moscow' AND town_to = 'Moscow') as y
        GROUP BY name) as p
    WHERE count > 1



9.  SELECT name, SUM(time_diff) as minute_fly
    FROM (
          SELECT name, abs(time_diff) as time_diff
          FROM (
                SELECT company.name,
                EXTRACT(EPOCH FROM time_in - time_out)*60 as time_diff
                FROM company
                INNER JOIN trip ON trip.comp_id = company.company_id
                GROUP BY company.name, time_in - time_out) as u) as p
    GROUP BY name



10. SELECT name
    FROM (
    SELECT passenger.name,
           COUNT(pass_in_trip.passenger_id) as count_poletov,
           COUNT(DISTINCT(company.name)) as count_company
           FROM passenger
           INNER JOIN pass_in_trip USING(passenger_id)
           INNER JOIN trip USING(trip_number)
           INNER JOIN company ON company.company_id = trip.comp_id
           GROUP BY passenger.name) as x
    WHERE count_company >= 2 AND count_poletov % count_company = 0