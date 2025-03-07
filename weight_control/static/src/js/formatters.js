/** @odoo-module **/

import { registry } from "@web/core/registry";
import { escape, intersperse, nbsp, sprintf } from "@web/core/utils/strings";
import { isBinarySize } from "@web/core/utils/binary";
import { session } from "@web/session";

import { markup } from "@odoo/owl";

/**
 * Returns a string representing a float.  The result takes into account the
 * user settings (to display the correct decimal separator).
 *
 * @param {number | false} value the value that should be formatted
 * @param {Object} [options]
 * @param {number[]} [options.digits] the number of digits that should be used,
 *   instead of the default digits precision in the field.
 * @param {boolean} [options.humanReadable] if true, large numbers are formatted
 *   to a human readable format.
 * @param {string} [options.decimalPoint] decimal separating character
 * @param {string} [options.thousandsSep] thousands separator to insert
 * @param {number[]} [options.grouping] array of relative offsets at which to
 *   insert `thousandsSep`. See `insertThousandsSep` method.
 * @param {boolean} [options.noTrailingZeros=false] if true, the decimal part
 *   won't contain unnecessary trailing zeros.
 * @returns {string}
 */
export function formatFloatBig(value, options = {}) {
    if (value === false) {
        return "";
    }
    if (options.humanReadable) {
        return humanNumber(value, options);
    }
    const grouping = options.grouping || l10n.grouping;
    const thousandsSep = "thousandsSep" in options ? options.thousandsSep : l10n.thousandsSep;
    const decimalPoint = "decimalPoint" in options ? options.decimalPoint : l10n.decimalPoint;
    let precision;
    if (options.digits && options.digits[1] !== undefined) {
        precision = options.digits[1];
    } else {
        precision = 6;
    }
    const formatted = (value || 0).toFixed(precision).split(".");
    formatted[0] = insertThousandsSep(formatted[0], thousandsSep, grouping);
    if (options.noTrailingZeros) {
        formatted[1] = formatted[1].replace(/0+$/, "");
    }
    return formatted[1] ? formatted.join(decimalPoint) : formatted[0];
}

registry
    .add("float_big", formatFloatBig);
