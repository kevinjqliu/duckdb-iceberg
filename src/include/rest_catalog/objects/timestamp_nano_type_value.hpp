
#pragma once

#include "yyjson.hpp"
#include "duckdb/common/string.hpp"
#include "duckdb/common/vector.hpp"
#include "duckdb/common/case_insensitive_map.hpp"

using namespace duckdb_yyjson;

namespace duckdb {
namespace rest_api_objects {

class TimestampNanoTypeValue {
public:
	TimestampNanoTypeValue();
	TimestampNanoTypeValue(const TimestampNanoTypeValue &) = delete;
	TimestampNanoTypeValue &operator=(const TimestampNanoTypeValue &) = delete;
	TimestampNanoTypeValue(TimestampNanoTypeValue &&) = default;
	TimestampNanoTypeValue &operator=(TimestampNanoTypeValue &&) = default;

public:
	static TimestampNanoTypeValue FromJSON(yyjson_val *obj);

public:
	string TryFromJSON(yyjson_val *obj);

public:
	string value;
};

} // namespace rest_api_objects
} // namespace duckdb
