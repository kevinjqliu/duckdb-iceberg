
#pragma once

#include "yyjson.hpp"
#include "duckdb/common/string.hpp"
#include "duckdb/common/vector.hpp"
#include "duckdb/common/case_insensitive_map.hpp"

using namespace duckdb_yyjson;

namespace duckdb {
namespace rest_api_objects {

class AssertViewUUID {
public:
	AssertViewUUID();
	AssertViewUUID(const AssertViewUUID &) = delete;
	AssertViewUUID &operator=(const AssertViewUUID &) = delete;
	AssertViewUUID(AssertViewUUID &&) = default;
	AssertViewUUID &operator=(AssertViewUUID &&) = default;

public:
	static AssertViewUUID FromJSON(yyjson_val *obj);

public:
	string TryFromJSON(yyjson_val *obj);

public:
	string type;
	string uuid;
};

} // namespace rest_api_objects
} // namespace duckdb
