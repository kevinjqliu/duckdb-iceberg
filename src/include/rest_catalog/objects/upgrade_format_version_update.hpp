
#pragma once

#include "yyjson.hpp"
#include "duckdb/common/string.hpp"
#include "duckdb/common/vector.hpp"
#include "duckdb/common/case_insensitive_map.hpp"
#include "rest_catalog/objects/base_update.hpp"

using namespace duckdb_yyjson;

namespace duckdb {
namespace rest_api_objects {

class UpgradeFormatVersionUpdate {
public:
	UpgradeFormatVersionUpdate();
	UpgradeFormatVersionUpdate(const UpgradeFormatVersionUpdate &) = delete;
	UpgradeFormatVersionUpdate &operator=(const UpgradeFormatVersionUpdate &) = delete;
	UpgradeFormatVersionUpdate(UpgradeFormatVersionUpdate &&) = default;
	UpgradeFormatVersionUpdate &operator=(UpgradeFormatVersionUpdate &&) = default;

public:
	static UpgradeFormatVersionUpdate FromJSON(yyjson_val *obj);

public:
	string TryFromJSON(yyjson_val *obj);

public:
	BaseUpdate base_update;
	int32_t format_version;
	string action;
	bool has_action = false;
};

} // namespace rest_api_objects
} // namespace duckdb
