import math

import streamlit as st

from models import Garment, load_garments, save_garments
from search_engine import search_inventory


def _parse_optional_number(value: str, label: str):
    if not value.strip():
        return None
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{label} must be a number or left blank.") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be a finite number or left blank.")
    return number


st.set_page_config(page_title="ThreadTruth", page_icon="🌿", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: #f7faf7;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #eef4ef;
    }
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #dce8df;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(32, 79, 49, 0.06);
    }
    [data-testid="stMetricLabel"] {
        color: #4f6656;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 920px;
    }
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1.25rem;
        }
        [data-testid="stMetric"] {
            padding: 12px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

garments = load_garments()
clothing_inventory = [garment.to_record() for garment in garments]

st.title("ThreadTruth")
st.caption("The price tag doesn't show the full environmental impact.")

page = st.sidebar.radio("Navigation", ["Aha! comparison", "About ThreadTruth"])

if page == "Aha! comparison":
    st.header("A closer look at your clothing")
    st.write("Move from the item you notice to the impact you may not see.")

    if st.session_state.get("last_saved_garment"):
        st.success(
            f"Saved **{st.session_state['last_saved_garment']}** to data.json. "
            "It is ready to compare below."
        )

    with st.expander("1  Add a clothing item", expanded=False):
        with st.form("add_garment_form"):
            garment_name = st.text_input("Name")
            garment_size = st.text_input("Size")
            water_input = st.text_input("Water impact (optional)")
            carbon_input = st.text_input("Carbon emissions (optional)")
            submitted = st.form_submit_button("Save & compare", use_container_width=True)

        if submitted:
            if not garment_name.strip() or not garment_size.strip():
                st.error("Enter both a clothing item name and size.")
            else:
                try:
                    water_impact = _parse_optional_number(water_input, "Water impact")
                    carbon_emissions = _parse_optional_number(
                        carbon_input, "Carbon emissions"
                    )
                except ValueError as error:
                    st.error(str(error))
                else:
                    new_garment = Garment(
                        name=garment_name.strip(),
                        size=garment_size.strip().upper(),
                        water_impact=water_impact,
                        carbon_emissions=carbon_emissions,
                    )
                    garments.append(new_garment)
                    save_garments(garments)
                    st.session_state["last_saved_garment"] = new_garment.name
                    st.session_state["selected_garment"] = new_garment
                    st.rerun()

    st.divider()
    st.subheader("2  Explore the comparison")

    selected_garment = st.selectbox(
        "Choose a clothing item",
        garments,
        key="selected_garment",
        format_func=lambda garment: f"{garment.name} ({garment.size})",
    )

    selected_record = selected_garment.to_record()
    result = search_inventory(
        [selected_record], selected_record["details"]["size"]
    )

    if result is None:
        st.warning("No matching clothing item was found in the inventory.")
    else:
        details = result["details"]
        water = details.get("water")
        carbon = details.get("carbon")
        waste = details.get("waste")

        st.caption(f"Comparing **{result['item']}** · Size **{details['size']}**")

        shopping_column, impact_column = st.columns(2, gap="medium")
        with shopping_column:
            st.markdown("### What usually stands out")
            st.warning(
                "**At the store, the visible choice is often:**\n\n"
                "• Price\n"
                "• Style\n"
                "• Fit and appearance"
            )

        with impact_column:
            st.markdown("### What the data reveals")
            st.success(f"Environmental impact recorded for **{result['item']}**")

        water_value = (
            f"{water:,} L"
            if isinstance(water, (int, float))
            else "Unavailable"
        )
        carbon_value = (
            f"{carbon:g} kg"
            if isinstance(carbon, (int, float))
            else "Unavailable"
        )
        waste_value = (
            f"{waste:g}"
            if isinstance(waste, (int, float))
            else "Unavailable"
        )

        metric_column_1, metric_column_2, metric_column_3 = st.columns(
            3, gap="medium"
        )
        with metric_column_1:
            st.metric("Water impact", water_value)
        with metric_column_2:
            st.metric("Carbon emissions", carbon_value)
        with metric_column_3:
            st.metric(
                "Textile waste",
                waste_value,
                help="Unit not specified in data.json.",
            )

        water_values = [
            clothing["details"].get("water")
            for clothing in clothing_inventory
            if isinstance(clothing["details"].get("water"), (int, float))
        ]
        highest_water = max(water_values, default=None)
        if (
            isinstance(water, (int, float))
            and isinstance(highest_water, (int, float))
            and highest_water > 0
        ):
            st.caption(
                f"Water impact relative to the inventory maximum "
                f"({highest_water:,} L)"
            )
            st.progress(min(max(water / highest_water, 0.0), 1.0))

        st.caption(
            "The values above come from data.json. Textile waste has no unit "
            "specified in the inventory."
        )

else:
    st.header("About ThreadTruth")
    st.write(
        "ThreadTruth shows the clothing impact values currently recorded in the project."
    )
    st.info(
        "Water, carbon, and any recorded textile-waste values are loaded from "
        "data.json. Textile-waste units are not specified."
    )
