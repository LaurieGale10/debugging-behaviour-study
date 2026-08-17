extract_category_dataframe <- function(df, category_codes) {
    #Function used for filtering each unit's code to a relevant category (used for calculating mv-alpha per category).
    category_dataframe <- df
    category_dataframe[] <- lapply(
        category_dataframe,
        function(coder_column) lapply(
            coder_column,
            function(codes) {
                matched_codes <- codes[codes %in% category_codes]
                if (length(matched_codes) == 0) NULL else matched_codes
            }
        )
    )

    category_dataframe
}

first_move_codes <- c(
    "Made changes before running code",
    "Ran code before making changes"
)

get_first_move_codes <- function() {
    first_move_codes
}

positive_debugging_indicator_codes <- c(
    "Entered incorrect input",
    "Made improvements to program",
    "First change on line referred to in error message"
)

get_positive_debugging_indicator_codes <- function() {
    positive_debugging_indicator_codes
}

added_error_codes <- c(
    "Reverted corrective change(s)",
    "Introduced additional syntax error(s)",
    "Incorrect syntactical changes to existing statements",
    "Incorrect syntactical changes to output statements",
    "Incorrect syntactical changes involving selection",
    "Incorrect syntactical changes involving iteration",
    "Incorrect syntactical changes to variable assignments",
    "Incorrect syntactical changes involving other statements in program",
    "Incorrect syntactical changes involving symbols",
    "Incorrect syntactical changes to operators",
    "Incorrect syntactical changes to mathematical operators",
    "Incorrect syntactical changes to logical operators",
    "Incorrect syntactical changes to other symbols",
    "Incorrect syntactical changes involving fusion or distribution of multiple lines of code",
    "Addition of non-Python strings",
    "Incorrect syntactical changes involving variable references",
    "Incorrect syntactical changes to whitespace of program",
    "Introduced runtime error(s)",
    "Incorrect semantic changes to variable assignments",
    "Incorrect semantic changes to variable references",
    "Incorrect semantic changes to other statements in program",
    "Introduced type error(s)",
    "Incorrect typewise changes involving variables",
    "Incorrect typewise changes to function call",
    "Incorrect typewise changes to other statements in program",
    "Introduced logical error(s)",
    "Logically incorrect changes involving output statements",
    "Logically incorrect changes to operators",
    "Logically incorrect changes to mathematical operators",
    "Logically incorrect changes to logical operators",
    "Logically incorrect changes involving variables",
    "Logically incorrect changes to program flow",
    "Logically incorrect changes to other statements"
)

get_added_error_codes <- function() {
    added_error_codes
}

resolved_error_codes <- c(
    "Resolved syntax error(s)",
    "Correctly resolved syntax error",
    "Resolved syntax error by changing syntax of erroneous component",
    "Introduced logical error from resolution of syntax error",
    "Hard-coded resolution of syntax error",
    "Resolved runtime error(s)",
    "Correctly resolved runtime error",
    "Introduced logical error from resolution of runtime error",
    "Hard-coded resolution of runtime error",
    "Resolved type error(s)",
    "Correctly resolved type error",
    "Hard-coded resolution of type error",
    "Resolved logical error(s)",
    "Correctly resolved logical error",
    "Correctly resolved logical error while code not running",
    "Correctly resolved logical error after a single successful run",
    "Correctly resolved logical error after repeated successful runs",
    "Hard-coded resolution of logical error"
)

get_resolved_error_codes <- function() {
    resolved_error_codes
}

inconsequential_change_codes <- c(
    "Addition/removal or editing of comments",
    "Inconsequential changes involving symbols",
    "Inconsequential changes to variable references",
    "Inconsequential changes to whitespace of program",
    "Changes to existing statements in the program",
    "Inconsequential changes to (existing) outputs",
    "Inconsequential changes to (existing) inputs",
    "Inconsequential changes to (existing) other statements",
    "Addition of unnecessary code"
)

get_inconsequential_change_codes <- function() {
    inconsequential_change_codes
}

miscellaneous_behaviour_codes <- c(
    "Repeated runs",
    "Repeatedly ran successfully executing program",
    "Repeatedly ran erroneous program",
    "Repeatedly ran program at beginning of exercise",
    "Reverted previous changes"
)

get_miscellaneous_behaviour_codes <- function() {
    miscellaneous_behaviour_codes
}

create_category_csv_with_agreement <- function(
    category_dataframe,
    coder1_col = 1,
    coder2_col = 2,
    both_empty_as_na = TRUE
) {
    if (coder1_col < 1 || coder1_col > ncol(category_dataframe) ||
        coder2_col < 1 || coder2_col > ncol(category_dataframe)) {
        stop("coder column indices are out of bounds")
    }

    to_str <- function(x) {
        if (is.null(x) || length(x) == 0) NA_character_ else paste(x, collapse = ";")
    }

    to_set <- function(x) {
        if (is.null(x) || length(x) == 0) {
            return(character(0))
        }

        values <- trimws(as.character(x))
        values <- values[nzchar(values)]
        unique(values)
    }

    is_empty_codes <- function(x) {
        is.null(x) || length(x) == 0
    }

    csv_df <- as.data.frame(lapply(category_dataframe, function(col) {
        vapply(col, to_str, character(1))
    }), stringsAsFactors = FALSE)

    coder1 <- category_dataframe[[coder1_col]]
    coder2 <- category_dataframe[[coder2_col]]

    n_agreements_fn <- function(a_set, b_set) {
        length(intersect(a_set, b_set))
    }

    n_disagreements_fn <- function(a_set, b_set) {
        length(setdiff(union(a_set, b_set), intersect(a_set, b_set)))
    }

    percentage_agreement_fn <- function(n_agreements, n_disagreements) {
        denominator <- n_agreements + n_disagreements
        if (denominator == 0) {
            return(NA_real_)
        }
        (n_agreements / denominator) * 100
    }

    row_metrics <- mapply(function(a, b) {
        if (both_empty_as_na && is_empty_codes(a) && is_empty_codes(b)) {
            return(list(
                n_agreements = NA_integer_,
                n_disagreements = NA_integer_,
                percentage_agreement = NA_real_
            ))
        }

        a_set <- to_set(a)
        b_set <- to_set(b)

        n_agreements <- n_agreements_fn(a_set, b_set)
        n_disagreements <- n_disagreements_fn(a_set, b_set)
        percentage_agreement <- percentage_agreement_fn(n_agreements, n_disagreements)

        list(
            n_agreements = n_agreements,
            n_disagreements = n_disagreements,
            percentage_agreement = percentage_agreement
        )
    }, coder1, coder2, USE.NAMES = FALSE, SIMPLIFY = FALSE)

    csv_df$n_agreements <- vapply(row_metrics, function(x) x$n_agreements, integer(1))
    csv_df$n_disagreements <- vapply(row_metrics, function(x) x$n_disagreements, integer(1))
    csv_df$percentage_agreement <- vapply(row_metrics, function(x) x$percentage_agreement, numeric(1))

    csv_df
}

calculate_total_agreement <- function(
    category_csv
) {
    total_agreements <- sum(category_csv[["n_agreements"]], na.rm = TRUE)
    total_disagreements <- sum(category_csv[["n_disagreements"]], na.rm = TRUE)
    denominator <- total_agreements + total_disagreements

    total_percentage_agreement <- if (denominator == 0) {
        NA_real_
    } else {
        (total_agreements / denominator) * 100
    }

    list(
        n_agreements = total_agreements,
        n_disagreements = total_disagreements,
        percentage_agreement = total_percentage_agreement
    )
}
