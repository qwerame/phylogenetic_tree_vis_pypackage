import csv
import json


# true代表二者有constraint关系， false代表二者重叠部分较大，没有constraint关系
def define_constraint(ref_start, ref_end, tgt_start, tgt_end, ref_name, tgt_name):
    min_pos = min(ref_start, tgt_start)
    max_pos = max(ref_end, tgt_end)
    if max_pos - min_pos >= ref_end - ref_start + tgt_end - tgt_start:
        return True

    else:
        overlap1 = (ref_end - ref_start + tgt_end - tgt_start - max_pos + min_pos) / (tgt_end - tgt_start)
        overlap2 = (ref_end - ref_start + tgt_end - tgt_start - max_pos + min_pos) / (ref_end - ref_start)
        overlap_mid = abs((ref_end - ref_start) / 2 - (tgt_end - tgt_start) / 2) / (tgt_end - tgt_start)

        returnValue = False if (overlap1 > 0.6 and overlap2 > 0.6) or (overlap2 > 0.7 and overlap_mid < 0.35) else True
        # print(f"{ref_name} {tgt_name} {overlap1} {overlap2} {overlap_mid} {returnValue}")
        return False if (overlap1 > 0.6 and overlap2 > 0.6) or (overlap2 > 0.7 and overlap_mid < 0.35) else True


def generateDirectionConstrains(min_attr, max_attr, mid_attr, len_attr, array, constraints):
    sorted_array = sorted(array, key=lambda x: x[len_attr])
    # print(list(map(lambda x: x['name'], sorted_array)))
    grouped = [False] * len(sorted_array)
    raw_return_value = []
    for i in range(len(sorted_array)):
        if grouped[i]:
            continue
        # print(sorted_array[i]["name"])
        position = sorted_array[i][mid_attr]
        locations = [{
            "name": sorted_array[i]["name"],
            "position": sorted_array[i][mid_attr]
        }]
        if i + 1 < len(sorted_array):
            for j in range(i + 1, len(sorted_array)):
                if (not grouped[j]
                        and not define_constraint(ref_start=sorted_array[i][min_attr],
                                                  ref_end=sorted_array[i][max_attr],
                                                  tgt_start=sorted_array[j][min_attr],
                                                  tgt_end=sorted_array[j][max_attr],
                                                  ref_name=sorted_array[i]["name"],
                                                  tgt_name=sorted_array[j]["name"])):
                    flag = False
                    if constraints is not None:
                        # print(f"{sorted_array[i]['name']} {constraints[sorted_array[i]['name']][0]}")
                        # print(f"{sorted_array[j]['name']} {constraints[sorted_array[j]['name']][0]}")
                        # print('\n')

                        for location in locations:
                            if constraints[location["name"]][0] == constraints[sorted_array[j]["name"]][0]:
                                flag = True
                                break
                    if flag is False:
                        locations.append({
                            "name": sorted_array[j]["name"],
                            "position": sorted_array[j][mid_attr]
                        })
                        grouped[j] = True
            raw_return_value.append({
                "group_position": position,
                "locations": locations
            })
        else:
            raw_return_value.append({
                "group_position": position,
                "locations": locations
            })

    # print("\n")
    sorted_return_value = list(
        map(lambda x: x["locations"], sorted(raw_return_value, key=lambda x: float(x["group_position"]))))
    all_sorted_return_value = list(map(lambda x: sorted(x, key=lambda y: float(y["position"])), sorted_return_value))
    # print(all_sorted_return_value)
    return list(map(lambda x: list(map(lambda y: y["name"], x)), all_sorted_return_value))


def generate_constraints(file_name, name_property, translation=None):
    """
       This function is used for uploading geojson file.

       Args:
       file_name (string): The location of the geojson file.
       name_property (string): The attr name indicating location.
       translation (string): The location of the csv file containing information about Chinese version of the location names.

       Returns:
       Constraints: The constraints info to be used in vis_info.
    """
    with open(file_name, 'r') as file:
        # 使用 json.load() 方法加载文件内容
        data = json.load(file)
        location_info = []
        for item in data["features"]:
            geometry = item["geometry"]
            properties = item["properties"]
            coordinates = [item for sublist in geometry["coordinates"] for item in sublist] \
                if geometry["type"] == "Polygon" \
                else [item for sublist in geometry["coordinates"] for finalList in sublist for item in finalList]

            longitudes = list(map(lambda x: x[0], coordinates))
            latitudes = list(map(lambda x: x[1], coordinates))

            location_info.append({
                "name": properties[name_property],
                "longitude_min": min(longitudes),
                "longitude_max": max(longitudes),
                "longitude_mid": sum(longitudes) / len(longitudes),
                "longitude_len": max(longitudes) - min(longitudes),
                "latitude_min": min(latitudes),
                "latitude_max": max(latitudes),
                "latitude_mid": sum(latitudes) / len(latitudes),
                "latitude_len": max(latitudes) - min(latitudes),
            })

        x_constraint = generateDirectionConstrains(min_attr="longitude_min",
                                                   max_attr="longitude_max",
                                                   mid_attr="longitude_mid",
                                                   len_attr="longitude_len",
                                                   array=location_info,
                                                   constraints=None)
        final_constraints = {}
        for index, group in enumerate(x_constraint):
            # print(index)
            # print(group)
            for location in group:
                final_constraints[location] = []
                final_constraints[location].append(index)
        # print(final_constraints)
        y_constraint = generateDirectionConstrains(min_attr="latitude_min",
                                                   max_attr="latitude_max",
                                                   mid_attr="latitude_mid",
                                                   len_attr="latitude_len",
                                                   array=location_info,
                                                   constraints=final_constraints)

        for index, group in enumerate(y_constraint[::-1]):
            for location in group:
                final_constraints[location].append(index)


        translation_map = {}
        if translation is None:
            for key in final_constraints.keys():
                translation_map[key] = key
        else:
            with open(translation, 'r') as csvfile:
                csvreader = csv.reader(csvfile)

                for row in csvreader:
                    translation_map[row[0]] = row[1]

        # file_path = 'output5_constraint.json'
        # with open(file_path, 'w', encoding="utf-8") as json_file:
        #     json.dump({"groups": final_constraints,
        #                "translation": translation_map,
        #                "info": {"rows": len(y_constraint), "columns": len(x_constraint)}},
        #               json_file, indent=4, ensure_ascii=False)

        return {
            "groups": final_constraints,
            "translation": translation_map,
            "info": {"rows": len(y_constraint), "columns": len(x_constraint)}
        }


# final_constraints = generateConstraints("africa.json", "NAME_2")

# final_constraints = generateConstraints("us-states.json", "name")

# generateConstraints("China_2.geojson", "name", "translation.csv")