import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { FeedTabs } from "@/components/feed-tabs";

describe("FeedTabs", () => {
  it("calls change handler when tab is clicked", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();
    render(<FeedTabs activeTab="for-you" onChange={onChange} />);
    await user.click(screen.getByRole("button", { name: "Finance" }));
    expect(onChange).toHaveBeenCalledWith("finance");
  });
});
